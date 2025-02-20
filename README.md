# **AI-Finance: AI-Powered Expense Prediction API**

## **Overview**
AI-Finance is a **FastAPI-based AI service** that leverages **machine learning (XGBoost)** to predict user spending patterns based on past financial behavior. The API processes financial data retrieved from **Firestore**, analyzes spending trends, and provides insights on **budget utilization, potential overspending, and future expense predictions**.

## **Key Features**
- **Budget Analysis**: Determines if a user has overspent or stayed within budget.
- **Category-Based Spending Insights**: Identifies which categories exceed their expected allocations.
- **Future Expense Prediction**: Uses an **XGBoost model** to forecast spending for the next cycle.
- **Savings Estimation**: Predicts potential savings and highlights excessive spending.
- **Budget Utilization Tracking**: Measures spending efficiency based on past trends.
- **Warnings & Alerts**: Detects **unusual spending behaviors** and provides recommendations.

---

## **Technology Stack**
- **FastAPI** - Lightweight and fast backend framework for API development.
- **XGBoost** - Machine learning model for predicting future expenses.
- **Firestore** - Cloud database for storing and retrieving user financial data.
- **Pandas** - Data processing and transformation for model input.
- **Python** - Backend implementation language.

---

## **How It Works**
### **1. Fetching User Financial Data**
The API retrieves **past transactions, budgets, and expenses** from **Firestore**.

### **2. Feature Engineering**
The system calculates key financial indicators such as:
- **Budget utilization**
- **Savings percentage**
- **Category-wise spending**
- **Historical budget trends**
- **Exceeded budget flags**

### **3. Expense Prediction with XGBoost**
- The **XGBoost model** is pre-trained using **historical transaction data**.
- When a request is made, the API prepares a **feature vector** and **feeds it into the model**.
- The model predicts **future expenses** and **potential savings**.

### **4. Generating Insights**
The API **compares past trends** with predicted spending and provides:
- Alerts for **over-budget spending**.
- Recommendations on **reducing expenses**.
- Insights into **spending habits**.

---

## **API Endpoints**
### **Predict Spending Trends**
**`POST /predict`**
#### **Request Format**
```json
{
  "user_id": "user123",
  "date_range": "this_month"
}
```

#### **Response Format**
```json
{
  "total_expenses": 1575,
  "exceeded_budget": 1,
  "exceeded_categories": {
    "Food & Entertainment": 125.0,
    "Shopping": 215.0,
    "Health & Wellness": 110.0
  },
  "expense_trend": "Overspent by $75.00",
  "spending_trend": "You have spent 105.0% of your budget.",
  "future_risk_prediction": "You might overspend by $1500.00 next period.",
  "savings": {
    "amount": -75,
    "percentage": "-5.0%"
  },
  "budget_utilization": {
    "percentage": "105.0%",
    "change": "95.00%"
  },
  "potential_savings": {
    "category": "Shopping",
    "saved_amount": 515
  },
  "constant_spending": {
    "category": "Other",
    "amount": 70
  },
  "top_spending_category": {
    "category": "Shopping",
    "amount": 515
  },
  "low_spending_category": {
    "category": "Other",
    "amount": 70
  },
  "predicted_future_expenses": 3000,
  "predicted_savings_next_month": 0,
  "abnormal_spending_alerts": [],
  "warnings": ["You have exceeded your budget by $75.00."],
  "total_budget": 1500,
  "categories": {
    "Essentials": 155,
    "Food & Entertainment": 425,
    "Shopping": 515,
    "Health & Wellness": 410,
    "Other": 70
  }
}
```

#### **Response Explanation**
- `"total_expenses": 1575` → User has spent **$1575** this month.
- `"exceeded_budget": 1` → The user **has overspent**.
- `"exceeded_categories"` → Lists **categories that went over budget**.
- `"future_risk_prediction": "You might overspend by $1500.00 next period."` → Predicts **next period's spending risk**.
- `"savings"` → Negative savings mean the **user is in debt**.
- `"budget_utilization"` → **105% usage** means spending exceeded the budget.
- `"warnings"` → Alerts the user about **excess spending**.

---

## **How to Run the API Locally**
### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/ai-finance.git
cd ai-finance
```

### **2. Set Up the Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate      # For Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Start the FastAPI Server**
```bash
uvicorn backend.ai_api:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Test API Using `cURL`**
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123", "date_range": "this_month"}'
```

### **6. View API Docs**
Once running, open:
```
http://127.0.0.1:8000/
```
This will display the API response.

---

## **Project Structure**
```
ai-finance/
│── backend/
│   │── ai_api.py       # FastAPI main entry file
│   │── ml/
│   │   │── predict_spending.py  # XGBoost model & prediction logic
│   │── utils/
│   │   │── firestore.py   # Firestore database interaction
│── resources/
│   │── ai_spending_model.json  # Pre-trained XGBoost model
│── requirements.txt
│── README.md
```

---

## **Machine Learning Model Details**
The **XGBoost model** (`ai_spending_model.json`) is trained on:
- **Historical expenses** per category.
- **Budget utilization trends**.
- **Savings and spending habits**.
- **Overspending risks**.

The model is **loaded into memory** when the API starts and runs predictions in real-time.