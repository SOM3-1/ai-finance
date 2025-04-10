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
    categories = data.categories

    savings = total_budget - total_expenses
    savings_percentage = (
        (savings / total_budget) * 100 if total_budget else 0
    )
    budget_utilization = (
        (total_expenses / total_budget) * 100 if total_budget else 0
    )
    exceeded_budget = 1 if total_expenses > total_budget else 0

    cat_count = len(categories) if len(categories) > 0 else 1
    category_alloc = total_budget / cat_count
    exceeded_categories = {}
    for name, cat_spend in categories.items():
        if cat_spend > category_alloc:
            exceeded_categories[name] = round(cat_spend - category_alloc, 2)

    df_input = pd.DataFrame([[
        total_budget,
        total_expenses,
        (total_expenses / total_budget) if total_budget else 0,
        savings_percentage
    ]],
    columns=["total_budget", "total_expenses", "budget_utilization", "savings_percentage"])
    current_utilization = (data.total_expenses / data.total_budget) * 100

    raw_pred = model.predict(df_input)[0]
    predicted_expenses = float(raw_pred)
    future_utilization = (predicted_expenses / data.total_budget) * 100
    utilization_change = future_utilization - current_utilization


    predicted_savings_next_month = total_budget - predicted_expenses

    diff = total_expenses - total_budget
    if diff > 0:
        expense_trend_msg = f"Overspent by ${diff:.2f} compared to your budget."
    elif diff < 0:
        expense_trend_msg = f"Under budget by ${abs(diff):.2f}."
    else:
        expense_trend_msg = "You exactly matched your budget."

    spending_trend_msg = (
        f"You have spent {round(budget_utilization, 2)}% of your budget."
    )

    future_diff = predicted_expenses - total_budget
    if future_diff > 0:
        future_risk_msg = f"You might overspend by ${future_diff:.2f} next period."
    elif future_diff < 0:
        future_risk_msg = f"You might have ${abs(future_diff):.2f} left in your budget next period."
    else:
        future_risk_msg = "Your future spending is projected to match your budget exactly."

    if categories:
        top_category = max(categories, key=categories.get)
        potential_savings_data = {
            "category": top_category,
            "saved_amount": round(categories[top_category], 2)
        }
    else:
        potential_savings_data = {
            "category": None,
            "saved_amount": 0
        }

    if categories:
        low_category = min(categories, key=categories.get)
        constant_spending_data = {
            "category": low_category,
            "amount": round(categories[low_category], 2)
        }
    else:
        constant_spending_data = {
            "category": None,
            "amount": 0
        }

    top_spending_category_data = None
    low_spending_category_data = None
    if categories:
        top_spending_category_data = {
            "category": top_category,
            "amount": round(categories[top_category], 2)
        }
        low_spending_category_data = {
            "category": low_category,
            "amount": round(categories[low_category], 2)
        }

    abnormal_spending_alerts = []
    for cat_name, cat_val in categories.items():
        if cat_val < 0:
            abnormal_spending_alerts.append(
                f"Category '{cat_name}' is negative ({cat_val}), possibly a refund or error."
            )
        if total_expenses > 0 and (cat_val / total_expenses) > 0.5:
            abnormal_spending_alerts.append(
                f"Category '{cat_name}' is over 50% of your total expenses—unusually high."
            )

    warnings_list = []
    if exceeded_budget:
        warnings_list.append(
            f"You have exceeded your budget by ${abs(savings):.2f}."
        )

    return {
        "total_expenses": round(total_expenses, 2),
        "exceeded_budget": exceeded_budget,
        "exceeded_categories": exceeded_categories,
        "expense_trend": expense_trend_msg,
        "spending_trend": spending_trend_msg,
        "future_risk_prediction": future_risk_msg,
        "savings": {
            "amount": round(savings, 2),
            "percentage": f"{round(savings_percentage, 2)}%"
        },
        "budget_utilization": {
            "percentage": f"{round(budget_utilization, 2)}%",
            "change": f"{utilization_change:.2f}%" 
        },
        "potential_savings": potential_savings_data,
        "constant_spending": constant_spending_data,
        "top_spending_category": top_spending_category_data,
        "low_spending_category": low_spending_category_data,
        "predicted_future_expenses": round(predicted_expenses, 2),
        "predicted_savings_next_month": round(predicted_savings_next_month, 2),
        "abnormal_spending_alerts": abnormal_spending_alerts,
        "warnings": warnings_list
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
