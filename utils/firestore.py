from firebase_config import db 
import datetime

def get_transactions_and_budgets(user_id, date_range):
    """ Fetch transactions and budgets from Firestore based on the date range. """

    today = datetime.date.today()
    
    if date_range == "this_month":
        start_date = today.replace(day=1)
    elif date_range == "past_month":
        start_date = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
    elif date_range == "past_3_months":
        start_date = (today.replace(day=1) - datetime.timedelta(days=90)).replace(day=1)
    else:
        start_date = datetime.date(2000, 1, 1) 

    transactions_ref = db.collection("transactions") \
        .where("userId", "==", user_id) \
        .where("date", ">=", str(start_date)) \
        .stream()

    budgets_ref = db.collection("budgets") \
        .where("userId", "==", user_id) \
        .where("fromDate", "<=", str(today)) \
        .where("toDate", ">=", str(start_date)) \
        .stream()

    total_expenses = sum(t.to_dict().get("amount", 0) for t in transactions_ref)
    total_budget = sum(b.to_dict().get("amount", 0) for b in budgets_ref)

    categories = {}
    for txn in transactions_ref:
        txn_data = txn.to_dict()
        category = txn_data.get("category", "Other")
        categories[category] = categories.get(category, 0) + txn_data.get("amount", 0)

    return {
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "categories": categories
    }
