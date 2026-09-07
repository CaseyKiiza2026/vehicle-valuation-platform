# Vehicle Valuation Platform

An end to end machine learning project that estimates advertised vehicle prices from vehicle identity, specifications, condition, usage, and location data.

## V1 Summary

| Item                  |                        Result |
| --------------------- | ----------------------------: |
| Working dataset       | 2,663,251 US vehicle listings |
| Model inputs          |                   21 features |
| Training observations |                     2,128,455 |
| Supported price range |               $1,000–$200,000 |
| Final model           |                      LightGBM |
| Test MAE              |                        $2,379 |
| Test RMSE             |                        $3,685 |
| Test R²               |                         0.956 |

## Technologies Used

| Area             |   Technologies                  |
| ---------------- | ------------------------------- |
| Data processing  | Python, pandas, NumPy           |
| Modeling         | scikit-learn, LightGBM, XGBoost |
| Analysis         | Jupyter Notebook, Matplotlib    |
| Model packaging  | Joblib                          |
| Version control  | Git, GitHub                     |

**Status:** V1 modeling and inference packaging are complete. The model and results are frozen, and no further tuning will be performed using the V1 test results.

## Project Approach

The project began with a Kaggle vehicle listings dataset. Exploratory data analysis found missing values, duplicate records, unrealistic mileage, inconsistent condition reporting, and suspicious prices.

The main data and modeling decisions were:

* Removed duplicate records and listings below $1,000.
* Removed columns that were empty or repeated information already available in another feature.
* Treated unrealistic mileage as missing instead of deleting complete vehicle records.
* Created indicators for missing or conflicting mileage, horsepower, owner-count, and condition information.
* Investigated suspicious prices by comparing listings with identical available features.
* Kept original model names after finding that grouping uncommon vehicles as `Rare` removed useful identity information.
* Split the data into training, validation, and test sets.
* Standardized numerical features, one-hot encoded categorical features, and passed boolean indicators through a `ColumnTransformer`.
* Compared regression models using validation MAE, RMSE, and R².

The final inputs include make, model, trim, year, mileage, horsepower, engine type, transmission, condition, ownership history, and city. After preprocessing, LightGBM used 10,521 transformed features.

## Why V1 Has a Defined Price Range

Error analysis showed that prediction errors increased for expensive vehicles because the dataset contained fewer high value examples. For example, only 291 validation listings were available in the $150,000–$200,000 price band.

Instead of claiming reliable performance across every vehicle price, I defined V1 around a supported range of **$1,000–$200,000**. V2 will focus on adding more high value vehicle data and expanding coverage toward $2 million.

## Progress From the Initial Baseline

The first Linear Regression baseline showed that the vehicle features contained useful pricing information, but error analysis exposed data quality problems and model limitations. After improving the data preparation, preserving important vehicle identity features, defining the V1 price range, and selecting LightGBM, validation performance improved significantly.

| Stage            | Model             | Validation MAE | Validation RMSE | Validation R² |
| ---------------- | ----------------- | -------------: | --------------: | ------------: |
| Initial baseline | Linear Regression |         $3,019 |          $5,356 |         0.922 |
| Final V1         | LightGBM          |         $2,380 |          $3,660 |         0.957 |

Compared with the initial baseline, the complete V1 pipeline reduced validation MAE by approximately **21%** and validation RMSE by approximately **32%**. This improvement reflects the combined effect of better data preparation, feature decisions, a defined operating range, and the final model not LightGBM alone.

## Model Comparison

| Model             | Validation MAE | Validation RMSE | Validation R² |
| ----------------- | -------------: | --------------: | ------------: |
| Linear Regression |         $2,958 |          $4,671 |         0.929 |
| Ridge Regression  |         $2,961 |          $4,665 |         0.930 |
| **LightGBM**      |     **$2,380** |      **$3,660** |     **0.957** |

Ridge performed almost identically to Linear Regression. LightGBM handled nonlinear relationships and interactions between vehicle features more effectively, reducing validation MAE by approximately **19.5%** compared with Linear Regression.

## Final Test Results

| Metric | Result |
| ------ | -----: |
| MAE    | $2,379 |
| RMSE   | $3,685 |
| R²     |  0.956 |

The validation and test results were close, showing that the final model performed consistently beyond the training data. These results are now the frozen V1 checkpoint.

Detailed evaluation results are available in [reports/v1_results.md](reports/v1_results.md).

## Reusable Inference

The fitted preprocessor and LightGBM model are saved in `models/v1/`. The inference code loads both artifacts and predicts the price of one valid vehicle record.

```python
from src.predict import predict_price

predicted_price = predict_price(vehicle)
print(f"Predicted listing price: ${predicted_price:,.2f}")
```

The `vehicle` input is a Python dictionary containing the 21 fields listed in `src/features.py`.

Inference flow:

1. `features.py` validates and orders the vehicle features.
2. The vehicle is converted into a one-row DataFrame.
3. The frozen preprocessor transforms the data.
4. The frozen LightGBM model returns the predicted price.

## Repository Guide

| Path                    | Purpose                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `notebooks/`            | EDA, feature engineering, baseline experiments, error analysis, and final V1 modeling |
| `src/features.py`       | Validates and prepares one vehicle record                                             |
| `src/predict.py`        | Loads the frozen artifacts and returns a prediction                                   |
| `models/v1/`            | Frozen preprocessor and LightGBM model                                                |
| `reports/v1_results.md` | Detailed V1 evaluation and figures                                                    |
| `requirements.txt`      | Python dependencies                                                                   |

Install the dependencies from the project root:

```bash
pip install -r requirements.txt
```

Large datasets and generated feature matrices are excluded from Git, while the two frozen V1 artifacts are included so inference can run without retraining.

## Limitations

* V1 predicts advertised listing prices, not final sale prices.
* The V1 modeling table does not include VINs, making some repeated listings difficult to confirm.
* The current inference function requires all 21 model features.
* The model does not yet provide a prediction range or confidence score.
* Vehicle markets change, so future versions will require newer data and retraining.

## Next Steps

* Add more exotic, classic, luxury, and high value vehicle data.
* Expand the supported range toward $2 million.
* Improve support for simple user inputs and missing information.
* Add prediction ranges or uncertainty estimates.
* Build an API and user interface around the inference code.
