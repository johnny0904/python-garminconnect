"""SQLAlchemy ORM models for Garmin health data."""

from datetime import date, datetime

from sqlalchemy import (
    BigInteger, Date, DateTime, Double, Float, ForeignKey,
    Integer, String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from johnny.db import Base


class DailySummary(Base):
    __tablename__ = "daily_summary"

    calendar_date: Mapped[date] = mapped_column(Date, primary_key=True)
    total_steps: Mapped[int | None] = mapped_column(Integer)
    total_distance_meters: Mapped[int | None] = mapped_column(Integer)
    daily_step_goal: Mapped[int | None] = mapped_column(Integer)
    total_kilocalories: Mapped[float | None] = mapped_column(Float)
    active_kilocalories: Mapped[float | None] = mapped_column(Float)
    bmr_kilocalories: Mapped[float | None] = mapped_column(Float)
    highly_active_seconds: Mapped[int | None] = mapped_column(Integer)
    active_seconds: Mapped[int | None] = mapped_column(Integer)
    sedentary_seconds: Mapped[int | None] = mapped_column(Integer)
    sleeping_seconds: Mapped[int | None] = mapped_column(Integer)
    moderate_intensity_minutes: Mapped[int | None] = mapped_column(Integer)
    vigorous_intensity_minutes: Mapped[int | None] = mapped_column(Integer)
    floors_ascended: Mapped[float | None] = mapped_column(Float)
    floors_descended: Mapped[float | None] = mapped_column(Float)
    min_heart_rate: Mapped[int | None] = mapped_column(Integer)
    max_heart_rate: Mapped[int | None] = mapped_column(Integer)
    resting_heart_rate: Mapped[int | None] = mapped_column(Integer)
    last_7d_avg_resting_hr: Mapped[int | None] = mapped_column(Integer)
    average_stress_level: Mapped[int | None] = mapped_column(Integer)
    max_stress_level: Mapped[int | None] = mapped_column(Integer)
    stress_duration: Mapped[int | None] = mapped_column(Integer)
    rest_stress_duration: Mapped[int | None] = mapped_column(Integer)
    low_stress_duration: Mapped[int | None] = mapped_column(Integer)
    medium_stress_duration: Mapped[int | None] = mapped_column(Integer)
    high_stress_duration: Mapped[int | None] = mapped_column(Integer)
    body_battery_charged: Mapped[int | None] = mapped_column(Integer)
    body_battery_drained: Mapped[int | None] = mapped_column(Integer)
    body_battery_highest: Mapped[int | None] = mapped_column(Integer)
    body_battery_lowest: Mapped[int | None] = mapped_column(Integer)
    body_battery_most_recent: Mapped[int | None] = mapped_column(Integer)
    body_battery_at_wake: Mapped[int | None] = mapped_column(Integer)
    body_battery_during_sleep: Mapped[int | None] = mapped_column(Integer)
    average_spo2: Mapped[float | None] = mapped_column(Float)
    lowest_spo2: Mapped[float | None] = mapped_column(Float)
    avg_waking_respiration: Mapped[float | None] = mapped_column(Float)
    highest_respiration: Mapped[float | None] = mapped_column(Float)
    lowest_respiration: Mapped[float | None] = mapped_column(Float)
    weight: Mapped[float | None] = mapped_column(Float)
    bmi: Mapped[float | None] = mapped_column(Float)
    body_fat: Mapped[float | None] = mapped_column(Float)
    body_water: Mapped[float | None] = mapped_column(Float)
    bone_mass: Mapped[float | None] = mapped_column(Float)
    muscle_mass: Mapped[float | None] = mapped_column(Float)
    visceral_fat: Mapped[float | None] = mapped_column(Float)
    metabolic_age: Mapped[float | None] = mapped_column(Float)
    hydration_value_ml: Mapped[int | None] = mapped_column(Integer)
    hydration_goal_ml: Mapped[int | None] = mapped_column(Integer)


class DailySleep(Base):
    __tablename__ = "daily_sleep"

    calendar_date: Mapped[date] = mapped_column(Date, primary_key=True)
    sleep_start_timestamp_local: Mapped[datetime | None] = mapped_column(DateTime)
    sleep_end_timestamp_local: Mapped[datetime | None] = mapped_column(DateTime)
    sleep_time_seconds: Mapped[int | None] = mapped_column(Integer)
    nap_time_seconds: Mapped[int | None] = mapped_column(Integer)
    deep_sleep_seconds: Mapped[int | None] = mapped_column(Integer)
    light_sleep_seconds: Mapped[int | None] = mapped_column(Integer)
    rem_sleep_seconds: Mapped[int | None] = mapped_column(Integer)
    awake_sleep_seconds: Mapped[int | None] = mapped_column(Integer)
    awake_count: Mapped[int | None] = mapped_column(Integer)
    avg_sleep_stress: Mapped[float | None] = mapped_column(Float)
    avg_heart_rate: Mapped[float | None] = mapped_column(Float)
    average_respiration: Mapped[float | None] = mapped_column(Float)
    lowest_respiration: Mapped[float | None] = mapped_column(Float)
    highest_respiration: Mapped[float | None] = mapped_column(Float)
    sleep_score_overall: Mapped[int | None] = mapped_column(Integer)
    sleep_score_qualifier: Mapped[str | None] = mapped_column(String(20))
    rem_percentage: Mapped[int | None] = mapped_column(Integer)
    light_percentage: Mapped[int | None] = mapped_column(Integer)
    deep_percentage: Mapped[int | None] = mapped_column(Integer)
    sleep_need_baseline_minutes: Mapped[int | None] = mapped_column(Integer)
    sleep_need_actual_minutes: Mapped[int | None] = mapped_column(Integer)
    body_battery_change: Mapped[float | None] = mapped_column(Float)
    resting_heart_rate: Mapped[float | None] = mapped_column(Float)
    avg_overnight_hrv: Mapped[float | None] = mapped_column(Float)


class DailyHrv(Base):
    __tablename__ = "daily_hrv"

    calendar_date: Mapped[date] = mapped_column(Date, primary_key=True)
    weekly_avg: Mapped[float | None] = mapped_column(Float)
    last_night_avg: Mapped[float | None] = mapped_column(Float)
    last_night_5min_high: Mapped[float | None] = mapped_column(Float)
    baseline_low_upper: Mapped[float | None] = mapped_column(Float)
    baseline_balanced_low: Mapped[float | None] = mapped_column(Float)
    baseline_balanced_upper: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str | None] = mapped_column(String(20))


class Activity(Base):
    __tablename__ = "activities"

    activity_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    calendar_date: Mapped[date | None] = mapped_column(Date, index=True)
    activity_name: Mapped[str | None] = mapped_column(String(255))
    activity_type_key: Mapped[str | None] = mapped_column(String(50))
    activity_type_id: Mapped[int | None] = mapped_column(Integer)
    start_time_local: Mapped[datetime | None] = mapped_column(DateTime)
    start_time_gmt: Mapped[datetime | None] = mapped_column(DateTime)
    distance_meters: Mapped[float | None] = mapped_column(Float)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    elapsed_duration_seconds: Mapped[float | None] = mapped_column(Float)
    moving_duration_seconds: Mapped[float | None] = mapped_column(Float)
    elevation_gain: Mapped[float | None] = mapped_column(Float)
    elevation_loss: Mapped[float | None] = mapped_column(Float)
    average_speed: Mapped[float | None] = mapped_column(Float)
    max_speed: Mapped[float | None] = mapped_column(Float)
    start_latitude: Mapped[float | None] = mapped_column(Double)
    start_longitude: Mapped[float | None] = mapped_column(Double)
    calories: Mapped[float | None] = mapped_column(Float)
    bmr_calories: Mapped[float | None] = mapped_column(Float)
    average_hr: Mapped[float | None] = mapped_column(Float)
    max_hr: Mapped[float | None] = mapped_column(Float)
    average_cadence: Mapped[float | None] = mapped_column(Float)
    max_cadence: Mapped[float | None] = mapped_column(Float)
    steps: Mapped[int | None] = mapped_column(Integer)
    avg_power: Mapped[float | None] = mapped_column(Float)
    max_power: Mapped[float | None] = mapped_column(Float)
    norm_power: Mapped[float | None] = mapped_column(Float)
    aerobic_training_effect: Mapped[float | None] = mapped_column(Float)
    anaerobic_training_effect: Mapped[float | None] = mapped_column(Float)
    vo2_max: Mapped[float | None] = mapped_column(Float)
    avg_vertical_oscillation: Mapped[float | None] = mapped_column(Float)
    avg_ground_contact_time: Mapped[float | None] = mapped_column(Float)
    avg_stride_length: Mapped[float | None] = mapped_column(Float)
    avg_vertical_ratio: Mapped[float | None] = mapped_column(Float)
    min_temperature: Mapped[float | None] = mapped_column(Float)
    max_temperature: Mapped[float | None] = mapped_column(Float)
    training_effect_label: Mapped[str | None] = mapped_column(String(50))
    activity_training_load: Mapped[float | None] = mapped_column(Float)
    fastest_split_1000: Mapped[float | None] = mapped_column(Float)
    fastest_split_1609: Mapped[float | None] = mapped_column(Float)
    fastest_split_5000: Mapped[float | None] = mapped_column(Float)
    fastest_split_10000: Mapped[float | None] = mapped_column(Float)
    hr_time_in_zone_1: Mapped[float | None] = mapped_column(Float)
    hr_time_in_zone_2: Mapped[float | None] = mapped_column(Float)
    hr_time_in_zone_3: Mapped[float | None] = mapped_column(Float)
    hr_time_in_zone_4: Mapped[float | None] = mapped_column(Float)
    hr_time_in_zone_5: Mapped[float | None] = mapped_column(Float)
    difference_body_battery: Mapped[int | None] = mapped_column(Integer)

    split_summaries: Mapped[list["ActivitySplitSummary"]] = relationship(
        back_populates="activity", cascade="all, delete-orphan"
    )


class ActivitySplitSummary(Base):
    __tablename__ = "activity_split_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("activities.activity_id"), index=True)
    split_type: Mapped[str | None] = mapped_column(String(30))
    no_of_splits: Mapped[float | None] = mapped_column(Float)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    distance_meters: Mapped[float | None] = mapped_column(Float)
    average_speed: Mapped[float | None] = mapped_column(Float)
    max_speed: Mapped[float | None] = mapped_column(Float)
    total_ascent: Mapped[float | None] = mapped_column(Float)
    elevation_loss: Mapped[float | None] = mapped_column(Float)

    activity: Mapped["Activity"] = relationship(back_populates="split_summaries")
