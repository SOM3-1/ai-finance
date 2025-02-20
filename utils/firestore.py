from firebase_config import db
import datetime
from google.cloud.firestore_v1.base_query import FieldFilter

def get_transactions_and_budgets(user_id, date_range):
    """ Fetch transactions and budgets for the requested period and all-time user data. """

    today = datetime.date.today()

    if date_range == "this_month":
        start_date = today.replace(day=1)  # Start of current month
    elif date_range == "past_month":
        start_date = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)  # Start of last full month
    elif date_range == "past_3_months":
        start_date = (today.replace(day=1) - datetime.timedelta(days=90)).replace(day=1)  # 3 months ago
    elif date_range == "past_6_months":
        start_date = (today.replace(day=1) - datetime.timedelta(days=180)).replace(day=1)  # 6 months ago
    elif date_range == "past_year":
        start_date = today.replace(year=today.year - 1, day=1) 
    else:
        start_date = datetime.date(2024, 1, 1) 

    transactions_list = list(db.collection("transactions")
        .where(filter=FieldFilter("userId", "==", user_id))
        .where(filter=FieldFilter("date", ">=", str(start_date)))
        .stream())

    budgets_list = list(db.collection("budgets")
        .where(filter=FieldFilter("userId", "==", user_id))
        .where(filter=FieldFilter("fromDate", "<=", str(today)))
        .where(filter=FieldFilter("toDate", ">=", str(start_date)))
        .stream())

    all_transactions_list = list(db.collection("transactions")
        .where(filter=FieldFilter("userId", "==", user_id))
        .stream())

    all_budgets_list = list(db.collection("budgets")
        .where(filter=FieldFilter("userId", "==", user_id))
        .stream())

    total_expenses = sum(t.to_dict().get("amount", 0) for t in transactions_list)
    total_budget = sum(b.to_dict().get("amount", 0) for b in budgets_list)

    all_expenses = sum(t.to_dict().get("amount", 0) for t in all_transactions_list)
    all_budget = sum(b.to_dict().get("amount", 0) for b in all_budgets_list)

    categories = {}
    for txn in transactions_list:
        txn_data = txn.to_dict()
        category = txn_data.get("category", "Other")
        categories[category] = categories.get(category, 0) + txn_data.get("amount", 0)

    all_categories = {}
    for txn in all_transactions_list:
        txn_data = txn.to_dict()
        category = txn_data.get("category", "Other")
        all_categories[category] = all_categories.get(category, 0) + txn_data.get("amount", 0)

    print("🔥 Firestore Data Retrieved:")
    print({
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "categories": categories,
        "all_time_expenses": all_expenses,
        "all_time_budget": all_budget,
        "all_time_categories": all_categories
    })

    return {
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "categories": categories,
        "all_time_expenses": all_expenses,
        "all_time_budget": all_budget,
        "all_time_categories": all_categories
    }
