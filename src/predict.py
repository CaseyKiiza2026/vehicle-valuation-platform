from pathlib import Path
import joblib
from src.features import build_feature_frame

PROJECT_ROOT = Path(__file__).resolve().parent.parent
V1_PATH = PROJECT_ROOT / "models" / "v1"
PREPROCESSOR_PATH = V1_PATH / "preprocessor.joblib"
MODEL_PATH = V1_PATH / "lightgbm.joblib"

preprocessor = joblib.load(PREPROCESSOR_PATH)
model = joblib.load(MODEL_PATH)

def predict_price(vehicle):
    feature_frame = build_feature_frame(vehicle)
    transformed_features = preprocessor.transform(feature_frame)
    predictions = model.predict(transformed_features)
    predicted_price = predictions[0]

    return float(predicted_price)
                                        
