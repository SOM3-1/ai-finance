from fastapi import APIRouter
from pydantic import BaseModel
from utils.firestore import get_transactions_and_budgets
from ml.predict_spending import predict_spending

router = APIRouter()

class PredictionRequest(BaseModel):
    user_id: str
    date_range: str

@router.post("/predict")
def predict(data: PredictionRequest):
    """ Fetches data from Firestore and predicts future spending trends. """

    finance_data = get_transactions_and_budgets(data.user_id, data.date_range)

    if finance_data["total_budget"] == 0:
        return {"error": "No budget data found for user"}

    prediction = predict_spending(
        finance_data["total_budget"],         
        finance_data["total_expenses"],       
        finance_data["categories"],            
        finance_data["all_time_expenses"],     
        finance_data["all_time_budget"],       
        finance_data["all_time_categories"],   
    )

    return prediction
