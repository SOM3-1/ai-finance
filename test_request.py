import requests

# API URL
url = "http://localhost:8000/predict"

# Example JSON request
payload = {
    "total_budget": 2510.84,
    "total_expenses": 2538.37,
    "categories": {
        "Essentials": 715.6,
        "Food & Entertainment": 634.97,
        "Shopping": 731.86,
        "Health & Wellness": 385.99,
        "Other": -420.06
    }
}

# Send request to FastAPI
response = requests.post(url, json=payload)

# Print response from API
print(response.json())
