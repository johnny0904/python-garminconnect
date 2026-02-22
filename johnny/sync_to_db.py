#!/usr/bin/env python3
"""Sync Garmin health data for a date to MySQL.

Usage:
    python johnny/sync_to_db.py [YYYY-MM-DD]

Defaults to yesterday if no date given.
Always fetches fresh data directly from the Garmin API.

Environment Variables:
    DATABASE_URL   (default: mysql+pymysql://healthuser:healthpassword@127.0.0.1:3307/health)
    EMAIL          Garmin account email
    PASSWORD       Garmin account password
    GARMINTOKENS   Path to token storage (default: ~/.garminconnect)
"""

import logging
import sys
from datetime import date, timedelta

from sqlalchemy import delete

from johnny.auth import init_api
from johnny.db import get_session, init_db
from johnny.models import ActivitySplitSummary
from johnny.parsers import (
    parse_activities,
    parse_daily_hrv,
    parse_daily_sleep,
    parse_daily_summary,
)

logging.getLogger("garminconnect").setLevel(logging.CRITICAL)


def _fetch(label: str, api_call):
    """Call api_call(), print progress, return result or None on error."""
    print(f"  Fetching {label}...", end=" ", flush=True)
    try:
        data = api_call()
        print("OK")
        return data
    except Exception as e:
        print(f"SKIPPED ({type(e).__name__}: {e})")
        return None


def main() -> None:
    # Parse date argument
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
        try:
            date.fromisoformat(target_date)
        except ValueError:
            print(f"Error: date must be YYYY-MM-DD, got '{target_date}'", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = (date.today() - timedelta(days=1)).isoformat()

    print(f"\n{'='*50}")
    print(f"Syncing Garmin data for: {target_date}")
    print(f"{'='*50}\n")

    print("Authenticating with Garmin Connect...")
    api = init_api()
    if api is None:
        print("ERROR: Could not authenticate with Garmin Connect.", file=sys.stderr)
        sys.exit(1)
    print("Authenticated.\n")

    # --- Fetch from API ---
    print("[Data Sources]")

    stats_body = _fetch("stats_and_body", lambda: api.get_stats_and_body(target_date))
    hydration = _fetch("hydration_data", lambda: api.get_hydration_data(target_date))
    sleep_data = _fetch("sleep_data", lambda: api.get_sleep_data(target_date))
    hrv_data = _fetch("hrv_data", lambda: api.get_hrv_data(target_date))
    activities_data = _fetch("activities_by_date", lambda: api.get_activities_by_date(target_date, target_date))

    # --- Parse ---
    print("\n[Parsing]")
    rows = {}

    if stats_body:
        rows["daily_summary"] = parse_daily_summary(stats_body, hydration)
        print(f"  daily_summary → {target_date}")

    if sleep_data:
        parsed_sleep = parse_daily_sleep(sleep_data)
        if parsed_sleep:
            rows["daily_sleep"] = parsed_sleep
            print(f"  daily_sleep   → {target_date}")

    if hrv_data:
        parsed_hrv = parse_daily_hrv(hrv_data)
        if parsed_hrv:
            rows["daily_hrv"] = parsed_hrv
            print(f"  daily_hrv     → {target_date}")

    activities = []
    if activities_data and isinstance(activities_data, list):
        activities = parse_activities(activities_data, target_date)
        print(f"  activities    → {len(activities)} activity/activities")

    if not rows and not activities:
        print("\nNothing to save.")
        return

    # --- Upsert to DB ---
    print("\n[Database]")
    init_db()

    session = get_session()
    try:
        for table_name, obj in rows.items():
            session.merge(obj)
            print(f"  Merged {table_name}")

        for act in activities:
            activity_id = act.activity_id
            # Snapshot split data as plain dicts before touching the ORM graph
            split_dicts = [
                {
                    "split_type": sp.split_type,
                    "no_of_splits": sp.no_of_splits,
                    "duration_seconds": sp.duration_seconds,
                    "distance_meters": sp.distance_meters,
                    "average_speed": sp.average_speed,
                    "max_speed": sp.max_speed,
                    "total_ascent": sp.total_ascent,
                    "elevation_loss": sp.elevation_loss,
                }
                for sp in act.split_summaries
            ]
            act.split_summaries.clear()

            # Delete existing splits, then upsert activity
            session.execute(
                delete(ActivitySplitSummary).where(
                    ActivitySplitSummary.activity_id == activity_id
                )
            )
            session.merge(act)
            session.flush()

            # Insert fresh split objects (avoids ORM cascade nulling the FK)
            for d in split_dicts:
                session.add(ActivitySplitSummary(activity_id=activity_id, **d))
            print(f"  Merged activity {activity_id} ({act.activity_name}) [{len(split_dicts)} splits]")

        session.commit()
        print("\nAll changes committed.")
    finally:
        session.close()

    # --- Summary ---
    print(f"\n{'='*50}")
    print(f"Done. Synced {target_date} to database.")
    tables_updated = list(rows.keys()) + (["activities"] if activities else [])
    print(f"Tables updated: {', '.join(tables_updated)}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
