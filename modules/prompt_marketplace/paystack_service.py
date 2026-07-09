import requests
from flask import current_app

PAYSTACK_BASE_URL = "https://api.paystack.co"


def initialize_transaction(email, amount_naira, callback_url, reference):
    """
    Initialize a Paystack transaction. Amount must be converted to kobo
    (Paystack's smallest currency unit) before sending.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "amount": amount_naira * 100,
        "callback_url": callback_url,
        "reference": reference,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)
    data = response.json()

    if response.status_code == 200 and data.get("status"):
        return {
            "success": True,
            "authorization_url": data["data"]["authorization_url"],
            "reference": data["data"]["reference"],
        }
    else:
        return {
            "success": False,
            "message": data.get("message", "Failed to initialize transaction."),
        }


def verify_transaction(reference):
    """
    Verify a Paystack transaction by its reference.
    Returns the transaction status and amount (in Naira) if successful.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
    }

    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()

    if response.status_code == 200 and data.get("status"):
        transaction_data = data["data"]
        return {
            "success": True,
            "status": transaction_data["status"],
            "amount_naira": transaction_data["amount"] // 100,
        }
    else:
        return {
            "success": False,
            "message": data.get("message", "Failed to verify transaction."),
        }