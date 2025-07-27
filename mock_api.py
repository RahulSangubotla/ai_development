# mock_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock Banking API")

# Mock Database
mock_db = {
    "users": {
        "user_123": {
            "name": "Anika Sharma",
            "accounts": {
                "acc_savings_01": {
                    "type": "Savings",
                    "balance": 50000.75,
                    "transactions": [
                        {"id": "txn_1", "desc": "Zomato Order", "amount": -450.00},
                        {"id": "txn_2", "desc": "Salary Credit", "amount": 75000.00},
                    ],
                }
            },
            "cards": {
                "card_456": {"number": "xxxx-xxxx-xxxx-1234", "status": "active"}
            },
        }
    }
}

# Pydantic models for request validation
class CardBlockRequest(BaseModel):
    user_id: str
    card_id: str

class LoanApplication(BaseModel):
    user_id: str
    loan_type: str
    amount: float

@app.post("/block-card")
def block_card(request: CardBlockRequest):
    """Blocks a user's credit/debit card."""
    user = mock_db["users"].get(request.user_id)
    if not user or request.card_id not in user["cards"]:
        raise HTTPException(status_code=404, detail="User or Card not found")
    
    user["cards"][request.card_id]["status"] = "blocked"
    print(f"INFO: Card {request.card_id} for user {request.user_id} has been blocked.")
    return {"message": f"Successfully blocked card {request.card_id}.", "status": "blocked"}

# The path for this GET request has been updated for clarity
@app.get("/get-statement/{user_id}/{account_id}")
def get_statement(user_id: str, account_id: str):
    """Retrieves a mini statement for a user's account."""
    user = mock_db["users"].get(user_id)
    if not user or account_id not in user["accounts"]:
        raise HTTPException(status_code=404, detail="User or Account not found")
    
    account = user["accounts"][account_id]
    return {
        "account_id": account_id,
        "balance": account["balance"],
        "recent_transactions": account["transactions"]
    }

@app.post("/apply-for-loan")
def apply_for_loan(application: LoanApplication):
    """Submits a loan application."""
    print(f"INFO: Received loan application for {application.user_id} for a {application.loan_type} loan of {application.amount}.")
    # In a real system, this would trigger a complex workflow.
    # Here, we just acknowledge the application.
    return {"message": "Loan application received and is under review.", "application_id": "loan_app_987"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)