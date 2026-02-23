"""Parsers converting raw Garmin JSON dicts to ORM model instances."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from johnny.models import Activity, ActivitySplitSummary, DailyHrv, DailySleep, DailySummary


def _sentinel(val: Any, *, allow_zero: bool = True) -> Any:
    """Return None for sentinel values (-1, -2) used by Garmin API."""
    if val is None:
        return None
    if isinstance(val, (int, float)) and val in (-1, -2):
        return None
    return val


def _epoch_ms_to_datetime(epoch_ms: int | None) -> datetime | None:
    """Convert epoch milliseconds to datetime, or None."""
    if epoch_ms is None:
        return None
    try:
        return datetime.fromtimestamp(int(epoch_ms) / 1000)
    except (OSError, OverflowError, ValueError):
        return None


def parse_daily_summary(
    stats_body: dict[str, Any],
    hydration: dict[str, Any] | None = None,
) -> DailySummary:
    """Parse stats_and_body.json (+ optional hydration_data.json) into DailySummary."""
    s = stats_body
    h = hydration or {}

    cal_date = date.fromisoformat(s["calendarDate"])

    return DailySummary(
        calendar_date=cal_date,
        total_steps=_sentinel(s.get("totalSteps")),
        total_distance_meters=_sentinel(s.get("totalDistanceMeters")),
        daily_step_goal=_sentinel(s.get("dailyStepGoal")),
        total_kilocalories=_sentinel(s.get("totalKilocalories")),
        active_kilocalories=_sentinel(s.get("activeKilocalories")),
        bmr_kilocalories=_sentinel(s.get("bmrKilocalories")),
        highly_active_seconds=_sentinel(s.get("highlyActiveSeconds")),
        active_seconds=_sentinel(s.get("activeSeconds")),
        sedentary_seconds=_sentinel(s.get("sedentarySeconds")),
        sleeping_seconds=_sentinel(s.get("sleepingSeconds")),
        moderate_intensity_minutes=_sentinel(s.get("moderateIntensityMinutes")),
        vigorous_intensity_minutes=_sentinel(s.get("vigorousIntensityMinutes")),
        floors_ascended=_sentinel(s.get("floorsAscended")),
        floors_descended=_sentinel(s.get("floorsDescended")),
        min_heart_rate=_sentinel(s.get("minHeartRate")),
        max_heart_rate=_sentinel(s.get("maxHeartRate")),
        resting_heart_rate=_sentinel(s.get("restingHeartRate")),
        last_7d_avg_resting_hr=_sentinel(s.get("lastSevenDaysAvgRestingHeartRate")),
        average_stress_level=_sentinel(s.get("averageStressLevel")),
        max_stress_level=_sentinel(s.get("maxStressLevel")),
        stress_duration=_sentinel(s.get("stressDuration")),
        rest_stress_duration=_sentinel(s.get("restStressDuration")),
        low_stress_duration=_sentinel(s.get("lowStressDuration")),
        medium_stress_duration=_sentinel(s.get("mediumStressDuration")),
        high_stress_duration=_sentinel(s.get("highStressDuration")),
        body_battery_charged=_sentinel(s.get("bodyBatteryChargedValue")),
        body_battery_drained=_sentinel(s.get("bodyBatteryDrainedValue")),
        body_battery_highest=_sentinel(s.get("bodyBatteryHighestValue")),
        body_battery_lowest=_sentinel(s.get("bodyBatteryLowestValue")),
        body_battery_most_recent=_sentinel(s.get("bodyBatteryMostRecentValue")),
        body_battery_at_wake=_sentinel(s.get("bodyBatteryAtWakeTime")),
        body_battery_during_sleep=_sentinel(s.get("bodyBatteryDuringSleep")),
        average_spo2=_sentinel(s.get("averageSpo2")),
        lowest_spo2=_sentinel(s.get("lowestSpo2")),
        avg_waking_respiration=_sentinel(s.get("avgWakingRespirationValue")),
        highest_respiration=_sentinel(s.get("highestRespirationValue")),
        lowest_respiration=_sentinel(s.get("lowestRespirationValue")),
        weight=_sentinel(s.get("weight")),
        bmi=_sentinel(s.get("bmi")),
        body_fat=_sentinel(s.get("bodyFat")),
        body_water=_sentinel(s.get("bodyWater")),
        bone_mass=_sentinel(s.get("boneMass")),
        muscle_mass=_sentinel(s.get("muscleMass")),
        visceral_fat=_sentinel(s.get("visceralFat")),
        metabolic_age=_sentinel(s.get("metabolicAge")),
        hydration_value_ml=_sentinel(h.get("valueInML")),
        hydration_goal_ml=_sentinel(h.get("goalInML")),
    )


def parse_daily_sleep(sleep_data: dict[str, Any]) -> DailySleep | None:
    """Parse sleep_data.json into DailySleep. Returns None if no DTO present."""
    dto = sleep_data.get("dailySleepDTO") or {}
    if not dto:
        return None

    cal_date_str = dto.get("calendarDate")
    if not cal_date_str:
        return None
    cal_date = date.fromisoformat(cal_date_str)

    scores = dto.get("sleepScores") or {}
    overall = scores.get("overall") or {}
    rem_pct = scores.get("remPercentage") or {}
    light_pct = scores.get("lightPercentage") or {}
    deep_pct = scores.get("deepPercentage") or {}

    sleep_need = dto.get("sleepNeed") or {}

    return DailySleep(
        calendar_date=cal_date,
        sleep_start_timestamp_local=_epoch_ms_to_datetime(dto.get("sleepStartTimestampGMT")),
        sleep_end_timestamp_local=_epoch_ms_to_datetime(dto.get("sleepEndTimestampGMT")),
        sleep_time_seconds=_sentinel(dto.get("sleepTimeSeconds")),
        nap_time_seconds=_sentinel(dto.get("napTimeSeconds")),
        deep_sleep_seconds=_sentinel(dto.get("deepSleepSeconds")),
        light_sleep_seconds=_sentinel(dto.get("lightSleepSeconds")),
        rem_sleep_seconds=_sentinel(dto.get("remSleepSeconds")),
        awake_sleep_seconds=_sentinel(dto.get("awakeSleepSeconds")),
        awake_count=_sentinel(dto.get("awakeCount")),
        avg_sleep_stress=_sentinel(dto.get("avgSleepStress")),
        avg_heart_rate=_sentinel(dto.get("avgHeartRate")),
        average_respiration=_sentinel(dto.get("averageRespirationValue")),
        lowest_respiration=_sentinel(dto.get("lowestRespirationValue")),
        highest_respiration=_sentinel(dto.get("highestRespirationValue")),
        sleep_score_overall=_sentinel(overall.get("value")),
        sleep_score_qualifier=overall.get("qualifierKey"),
        rem_percentage=_sentinel(rem_pct.get("value")),
        light_percentage=_sentinel(light_pct.get("value")),
        deep_percentage=_sentinel(deep_pct.get("value")),
        sleep_need_baseline_minutes=_sentinel(sleep_need.get("baseline")),
        sleep_need_actual_minutes=_sentinel(sleep_need.get("actual")),
        body_battery_change=_sentinel(sleep_data.get("bodyBatteryChange")),
        resting_heart_rate=_sentinel(sleep_data.get("restingHeartRate")),
        avg_overnight_hrv=_sentinel(sleep_data.get("avgOvernightHrv")),
    )


def parse_daily_hrv(hrv_data: dict[str, Any]) -> DailyHrv | None:
    """Parse hrv_data.json into DailyHrv. Returns None if no summary present."""
    summary = hrv_data.get("hrvSummary") or {}
    if not summary:
        return None

    cal_date_str = summary.get("calendarDate")
    if not cal_date_str:
        return None
    cal_date = date.fromisoformat(cal_date_str)

    baseline = summary.get("baseline") or {}

    return DailyHrv(
        calendar_date=cal_date,
        weekly_avg=_sentinel(summary.get("weeklyAvg")),
        last_night_avg=_sentinel(summary.get("lastNightAvg")),
        last_night_5min_high=_sentinel(summary.get("lastNight5MinHigh")),
        baseline_low_upper=_sentinel(baseline.get("lowUpper")) if isinstance(baseline, dict) else None,
        baseline_balanced_low=_sentinel(baseline.get("balancedLow")) if isinstance(baseline, dict) else None,
        baseline_balanced_upper=_sentinel(baseline.get("balancedUpper")) if isinstance(baseline, dict) else None,
        status=summary.get("status"),
    )


def parse_activities(
    activities_by_date: list[dict[str, Any]],
    target_date: str,
) -> list[Activity]:
    """Parse activities_by_date.json list into Activity ORM instances (with splits)."""
    results: list[Activity] = []

    for a in activities_by_date:
        act_type = a.get("activityType") or {}

        def _parse_dt(s: str | None) -> datetime | None:
            if not s:
                return None
            try:
                return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None

        activity = Activity(
            activity_id=a["activityId"],
            calendar_date=date.fromisoformat(target_date),
            activity_name=a.get("activityName"),
            activity_type_key=act_type.get("typeKey"),
            activity_type_id=act_type.get("typeId"),
            start_time_local=_parse_dt(a.get("startTimeLocal")),
            start_time_gmt=_parse_dt(a.get("startTimeGMT")),
            distance_meters=_sentinel(a.get("distance")),
            duration_seconds=_sentinel(a.get("duration")),
            elapsed_duration_seconds=_sentinel(a.get("elapsedDuration")),
            moving_duration_seconds=_sentinel(a.get("movingDuration")),
            elevation_gain=_sentinel(a.get("elevationGain")),
            elevation_loss=_sentinel(a.get("elevationLoss")),
            average_speed=_sentinel(a.get("averageSpeed")),
            max_speed=_sentinel(a.get("maxSpeed")),
            start_latitude=_sentinel(a.get("startLatitude")),
            start_longitude=_sentinel(a.get("startLongitude")),
            calories=_sentinel(a.get("calories")),
            bmr_calories=_sentinel(a.get("bmrCalories")),
            average_hr=_sentinel(a.get("averageHR")),
            max_hr=_sentinel(a.get("maxHR")),
            average_cadence=_sentinel(a.get("averageRunningCadenceInStepsPerMinute")),
            max_cadence=_sentinel(a.get("maxRunningCadenceInStepsPerMinute")),
            steps=_sentinel(a.get("steps")),
            avg_power=_sentinel(a.get("avgPower")),
            max_power=_sentinel(a.get("maxPower")),
            norm_power=_sentinel(a.get("normPower")),
            aerobic_training_effect=_sentinel(a.get("aerobicTrainingEffect")),
            anaerobic_training_effect=_sentinel(a.get("anaerobicTrainingEffect")),
            vo2_max=_sentinel(a.get("vO2MaxValue")),
            avg_vertical_oscillation=_sentinel(a.get("avgVerticalOscillation")),
            avg_ground_contact_time=_sentinel(a.get("avgGroundContactTime")),
            avg_stride_length=_sentinel(a.get("avgStrideLength")),
            avg_vertical_ratio=_sentinel(a.get("avgVerticalRatio")),
            min_temperature=_sentinel(a.get("minTemperature")),
            max_temperature=_sentinel(a.get("maxTemperature")),
            training_effect_label=a.get("trainingEffectLabel"),
            activity_training_load=_sentinel(a.get("activityTrainingLoad")),
            fastest_split_1000=_sentinel(a.get("fastestSplit_1000")),
            fastest_split_1609=_sentinel(a.get("fastestSplit_1609")),
            fastest_split_5000=_sentinel(a.get("fastestSplit_5000")),
            fastest_split_10000=_sentinel(a.get("fastestSplit_10000")),
            hr_time_in_zone_1=_sentinel(a.get("hrTimeInZone_1")),
            hr_time_in_zone_2=_sentinel(a.get("hrTimeInZone_2")),
            hr_time_in_zone_3=_sentinel(a.get("hrTimeInZone_3")),
            hr_time_in_zone_4=_sentinel(a.get("hrTimeInZone_4")),
            hr_time_in_zone_5=_sentinel(a.get("hrTimeInZone_5")),
            difference_body_battery=_sentinel(a.get("differenceBodyBattery")),
        )

        # Parse split summaries if present
        for sp in a.get("splitSummaries") or []:
            activity.split_summaries.append(
                ActivitySplitSummary(
                    split_type=sp.get("splitType"),
                    no_of_splits=_sentinel(sp.get("noOfSplits")),
                    duration_seconds=_sentinel(sp.get("duration")),
                    distance_meters=_sentinel(sp.get("distance")),
                    average_speed=_sentinel(sp.get("averageSpeed")),
                    max_speed=_sentinel(sp.get("maxSpeed")),
                    total_ascent=_sentinel(sp.get("totalAscent")),
                    elevation_loss=_sentinel(sp.get("elevationLoss")),
                )
            )

        results.append(activity)

    return results
