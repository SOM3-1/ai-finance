import json
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from pathlib import Path

def main():
    resources_path = Path(__file__).resolve().parent.parent / "resources"
    dataset_path = resources_path / "financial_dataset.json"
    model_path = resources_path / "ai_spending_model.json"

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    with open(dataset_path, "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    if "categories.Essentials" in df.columns:
        df.rename(columns={
            "categories.Essentials": "Essentials",
            "categories.Food & Entertainment": "Food_Entertainment",
            "categories.Shopping": "Shopping",
            "categories.Health & Wellness": "Health_Wellness",
            "categories.Other": "Other"
        }, inplace=True)

    df["budget_utilization"] = df["total_expenses"] / df["total_budget"]
    df["savings"] = df["total_budget"] - df["total_expenses"]
    df["savings_percentage"] = (df["savings"] / df["total_budget"]) * 100

    # 💡 NEW: Include historical features
    df["all_time_expenses"] = df.groupby("user_id")["total_expenses"].cumsum()
    df["all_time_budget"] = df.groupby("user_id")["total_budget"].cumsum()
    df["historical_budget_utilization"] = df["all_time_expenses"] / df["all_time_budget"]

    # Predict future spending
    df["predicted_future_expenses"] = df.groupby("user_id")["total_expenses"].shift(-1)
    df["predicted_future_expenses"] = df["predicted_future_expenses"].fillna(df["total_expenses"])

    features = [
        "total_budget",
        "total_expenses",
        "budget_utilization",
        "savings_percentage",
        "all_time_expenses", 
        "all_time_budget",  
        "historical_budget_utilization" 
    ]
    target = "predicted_future_expenses"

    df.dropna(subset=[target], inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(
        df[features],
        df[target],
        test_size=0.2,
        random_state=42
    )

    model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = (abs(preds - y_test)).mean()
    print(f"Mean Absolute Error: {mae:.2f}")

    model.save_model(str(model_path))
    print("Model training complete. Saved as ai_spending_model.json")

if __name__ == "__main__":
    main()