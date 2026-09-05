from typing import Any

import pandas as pd


MODEL_FEATURES = [
    "city",
    "make_name",
    "model_name",
    "trim_name",
    "engine_type",
    "frame_damaged",
    "fuel_type",
    "has_accidents",
    "salvage",
    "transmission",
    "wheel_system",
    "horsepower",
    "mileage",
    "owner_count",
    "year",
    "is_new",
    "mileage_missing",
    "horsepower_missing",
    "Condition_reported",
    "new_mileage_conflict",
    "used_owner_count_missing",
]


def build_feature_frame(vehicle: dict[str, Any]) -> pd.DataFrame:
    missing_features = [
        feature
        for feature in MODEL_FEATURES
        if feature not in vehicle
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    ordered_vehicle = {
        feature: vehicle[feature]
        for feature in MODEL_FEATURES
    }

    return pd.DataFrame([ordered_vehicle])