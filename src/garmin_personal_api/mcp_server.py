"""MCP server exposing Garmin Connect Personal API tools."""

from __future__ import annotations

import base64
import json
import logging
from datetime import date

from mcp.server.mcpserver import MCPServer

from .api_keys import resolve_api_key
from .auth import PersonalApiAuthenticator
from .client import GarminPersonalApiClient
from .errors import GarminPersonalApiError, HttpError

_LOGGER = logging.getLogger(__name__)

mcp = MCPServer(
    "Garmin Connect Personal API",
    instructions=(
        "Access Garmin Connect health and fitness data through the Personal API. "
        "Tools cover daily summaries, sleep, steps, stress, heart rate, HRV, SpO2, "
        "body battery, hydration, weight, nutrition, fitness age, activities, and more. "
        "All date parameters use YYYY-MM-DD format."
    ),
)

_authenticator: PersonalApiAuthenticator | None = None
_client: GarminPersonalApiClient | None = None


def _get_client() -> GarminPersonalApiClient:
    global _authenticator, _client
    if _client is not None:
        return _client
    api_key = resolve_api_key()
    _authenticator = PersonalApiAuthenticator()
    token = _authenticator.obtain_token(api_key)
    _client = GarminPersonalApiClient(token.access_token)
    return _client


def _format(data: object) -> str:
    if data is None:
        return "No data returned."
    return json.dumps(data, indent=2, default=str)


def _today() -> str:
    return date.today().isoformat()


# --- Tools ---


@mcp.tool()
def get_user_profile_settings() -> str:
    """Get the current user's Garmin profile settings including display name, units, and preferences."""
    return _format(_get_client().get_user_profile_settings())


@mcp.tool()
def get_daily_steps(start_date: str, end_date: str) -> str:
    """Get daily step counts for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_steps(start_date, end_date))


@mcp.tool()
def get_daily_sleep(calendar_date: str | None = None) -> str:
    """Get detailed sleep data for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_daily_sleep(calendar_date or _today()))


@mcp.tool()
def get_daily_sleep_summaries(start_date: str, end_date: str) -> str:
    """Get sleep summaries for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_sleep_summaries(start_date, end_date))


@mcp.tool()
def get_daily_stress(start_date: str, end_date: str) -> str:
    """Get daily stress levels for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_stress(start_date, end_date))


@mcp.tool()
def get_daily_heart_rate(calendar_date: str | None = None) -> str:
    """Get heart rate data for a specific date including resting HR and time-series readings.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_daily_heart_rate(calendar_date or _today()))


@mcp.tool()
def get_daily_hrv(calendar_date: str | None = None) -> str:
    """Get heart rate variability (HRV) data for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_daily_hrv(calendar_date or _today()))


@mcp.tool()
def get_daily_hrv_summaries(start_date: str, end_date: str) -> str:
    """Get daily HRV summaries for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_hrv_summaries(start_date, end_date))


@mcp.tool()
def get_heart_rate_zones() -> str:
    """Get the user's heart rate zones configuration."""
    return _format(_get_client().get_heart_rate_zones())


@mcp.tool()
def get_daily_body_battery(start_date: str, end_date: str, chunks: int | None = None) -> str:
    """Get Body Battery data for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
        chunks: Optional number of chunks to divide the data into
    """
    return _format(_get_client().get_daily_body_battery(start_date, end_date, chunks=chunks))


@mcp.tool()
def get_daily_spo2(calendar_date: str | None = None) -> str:
    """Get SpO2 (blood oxygen) data for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_daily_spo2(calendar_date or _today()))


@mcp.tool()
def get_daily_hydration(start_date: str, end_date: str) -> str:
    """Get daily hydration data for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_hydration(start_date, end_date))


@mcp.tool()
def get_daily_summaries(start_date: str, end_date: str) -> str:
    """Get comprehensive daily summaries (steps, calories, distance, etc.) for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_daily_summaries(start_date, end_date))


@mcp.tool()
def get_daily_food_logs(calendar_date: str | None = None) -> str:
    """Get nutrition/food log entries for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_daily_food_logs(calendar_date or _today()))


@mcp.tool()
def get_weight_measurements(start_date: str, end_date: str) -> str:
    """Get weight measurements for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_weight_measurements(start_date, end_date))


@mcp.tool()
def get_effective_weight_goals(start_date: str, end_date: str) -> str:
    """Get effective weight goals for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_effective_weight_goals(start_date, end_date))


@mcp.tool()
def get_fitness_age(calendar_date: str | None = None) -> str:
    """Get fitness age data for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_fitness_age(calendar_date or _today()))


@mcp.tool()
def get_wellness_activity_summaries(start_date: str, end_date: str) -> str:
    """Get wellness activity summaries for a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD), inclusive
    """
    return _format(_get_client().get_wellness_activity_summaries(start_date, end_date))


@mcp.tool()
def get_menstrual_cycle_summary(calendar_date: str | None = None) -> str:
    """Get menstrual cycle summary for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
    """
    return _format(_get_client().get_menstrual_cycle_summary(calendar_date or _today()))


@mcp.tool()
def get_menstrual_cycle_day_view(
    calendar_date: str | None = None, today_date: str | None = None
) -> str:
    """Get menstrual cycle day view for a specific date.

    Args:
        calendar_date: Date (YYYY-MM-DD), defaults to today
        today_date: Today's date (YYYY-MM-DD), defaults to today
    """
    return _format(
        _get_client().get_menstrual_cycle_day_view(
            calendar_date or _today(), today_date or _today()
        )
    )


@mcp.tool()
def search_activities(
    start: int = 0,
    limit: int = 20,
    start_date: str | None = None,
    end_date: str | None = None,
    activity_type: str | None = None,
) -> str:
    """Search for activities with optional filters.

    Args:
        start: Pagination offset (default 0)
        limit: Max results to return (default 20)
        start_date: Filter by start date (YYYY-MM-DD)
        end_date: Filter by end date (YYYY-MM-DD)
        activity_type: Filter by activity type (e.g. "running", "cycling")
    """
    return _format(
        _get_client().search_activities(
            start=start,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            activity_type=activity_type,
        )
    )


@mcp.tool()
def get_activity(activity_id: str) -> str:
    """Get detailed information about a specific activity.

    Args:
        activity_id: The activity ID (numeric)
    """
    return _format(_get_client().get_activity(activity_id))


@mcp.tool()
def get_activity_workouts(activity_id: str) -> str:
    """Get workout details for a specific activity.

    Args:
        activity_id: The activity ID (numeric)
    """
    return _format(_get_client().get_activity_workouts(activity_id))


@mcp.tool()
def download_activity(activity_id: str) -> str:
    """Download the original activity file (returns base64-encoded ZIP).

    Args:
        activity_id: The activity ID (numeric, must be positive)
    """
    content = _get_client().download_activity(activity_id)
    return base64.b64encode(content).decode("ascii")


@mcp.tool()
def refresh_token() -> str:
    """Force-refresh the Garmin bearer token. Use if requests are failing with 401."""
    global _authenticator, _client
    api_key = resolve_api_key()
    if _authenticator is None:
        _authenticator = PersonalApiAuthenticator()
    token = _authenticator.obtain_token(api_key, force_refresh=True)
    if _client is not None:
        _client.update_bearer_token(token.access_token)
    else:
        _client = GarminPersonalApiClient(token.access_token)
    return "Bearer token refreshed successfully."


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
