"""Shared Garmin Connect authentication helpers."""

import os
import sys
from getpass import getpass
from pathlib import Path

import requests
from garth.exc import GarthException, GarthHTTPError

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)


def get_credentials() -> tuple[str, str]:
    """Get email and password from environment or user input."""
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if not email:
        email = input("Login email: ")
    if not password:
        password = getpass("Enter password: ")
    return email, password


def init_api() -> Garmin | None:
    """Initialize Garmin API, trying stored tokens then interactive login."""
    tokenstore = os.getenv("GARMINTOKENS", "~/.garminconnect")
    tokenstore_path = Path(tokenstore).expanduser()

    try:
        garmin = Garmin()
        garmin.login(str(tokenstore_path))
        return garmin
    except (
        FileNotFoundError,
        GarthHTTPError,
        GarminConnectAuthenticationError,
        GarminConnectConnectionError,
    ):
        pass

    while True:
        try:
            email, password = get_credentials()
            garmin = Garmin(
                email=email, password=password, is_cn=False, return_on_mfa=True
            )
            result1, result2 = garmin.login()

            if result1 == "needs_mfa":
                mfa_code = input("Please enter your MFA code: ")
                try:
                    garmin.resume_login(result2, mfa_code)
                except GarthHTTPError as garth_error:
                    error_str = str(garth_error)
                    if "429" in error_str and "Too Many Requests" in error_str:
                        sys.exit(1)
                    elif "401" in error_str or "403" in error_str:
                        continue
                    else:
                        sys.exit(1)
                except GarthException:
                    continue

            garmin.garth.dump(str(tokenstore_path))
            return garmin

        except GarminConnectAuthenticationError:
            continue
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectConnectionError,
            requests.exceptions.HTTPError,
        ):
            return None
        except KeyboardInterrupt:
            return None
