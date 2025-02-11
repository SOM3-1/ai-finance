from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import pandas as pd

app = FastAPI()

model = xgb.XGBRegressor()
model.load_model("ai_spending_model.json")

class FinanceData(BaseModel):
    user_id: int
    date_range: str
    total_budget: float
    total_expenses: float
    categories: dict 

@app.post("/predict")
def predict_spending(data: FinanceData):
    total_budget = data.total_budget
    total_expenses = data.total_expenses

    budget_utilization = total_expenses / total_budget if total_budget else 0
    savings = total_budget - total_expenses
    savings_percentage = (savings / total_budget) * 100 if total_budget else 0

    inference_df = pd.DataFrame(
        [[total_budget, total_expenses, budget_utilization, savings_percentage]],
        columns=["total_budget", "total_expenses", "budget_utilization", "savings_percentage"]
    )

    predicted_expenses = model.predict(inference_df)[0]

    exceeded_budget = total_expenses > total_budget
    warnings = []
    if exceeded_budget:
        warnings.append(f"You have exceeded your budget by ${abs(savings):.2f}.")

    return {
        "user_id": data.user_id,
        "date_range": data.date_range,
        "total_expenses": total_expenses,
        "predicted_future_expenses": float(predicted_expenses),
        "budget_utilization": round(budget_utilization * 100, 2),
        "savings_percentage": round(savings_percentage, 2),
        "exceeded_budget": exceeded_budget,
        "warnings": warnings
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
