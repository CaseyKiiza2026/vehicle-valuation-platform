import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.predict import predict_price


logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Vehicle Price Prediction API")


class VehicleInputs(BaseModel):
    city: str
    make_name: str
    model_name: str
    trim_name: str
    engine_type: str

    # These were categorical strings during training.
    frame_damaged: str
    fuel_type: str
    has_accidents: str
    salvage: str

    transmission: str
    wheel_system: str

    horsepower: float
    mileage: float
    owner_count: float
    year: int

    # Preserve the original boolean/integer indicator types.
    is_new: bool
    mileage_missing: int
    horsepower_missing: int
    Condition_reported: bool
    new_mileage_conflict: bool
    used_owner_count_missing: bool


class PredictedOutputs(BaseModel):
    predicted_price: float


@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/predict", response_model=PredictedOutputs)
def predict(vehicle: VehicleInputs):
    try:
        vehicle_data = vehicle.model_dump()

        # Do not convert every boolean into an integer.
        prediction = predict_price(vehicle_data)

        return PredictedOutputs(predicted_price=float(prediction))

    except Exception as exc:
        logger.exception("Vehicle prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. See the server terminal for the traceback.",
        ) from exc