# seed_db.py
from pymongo import MongoClient

# --- Connection to MongoDB ---
client = MongoClient('mongodb://localhost:27017/')
db = client['banking_db']
users_collection = db['users']

# --- Expanded Mock Data ---
# A list containing multiple user documents
mock_users = [
    {
        "id": "user_123",
        "name": "Anika Sharma",
        "accounts": {
            "acc_savings_01": {
                "account_number": "409000000001",
                "type": "Savings",
                "balance": 50000.75,
                "transactions": [
                    {"id": "txn_1", "desc": "Zomato Order", "amount": -450.00},
                    {"id": "txn_2", "desc": "Salary Credit", "amount": 75000.00},
                ],
            },
            "acc_checking_02": {
                "account_number": "409000000002",
                "type": "Checking",
                "balance": 15230.20,
                "transactions": [
                    {"id": "txn_3", "desc": "Swiggy Instamart", "amount": -1200.50}
                ]
            }
        },
        "cards": {
            "card_debit_456": {"number": "xxxx-xxxx-xxxx-1234", "type": "Debit", "status": "active"},
            "card_credit_789": {"number": "xxxx-xxxx-xxxx-5678", "type": "Credit", "status": "active"}
        },
        "loans": {
            "loan_auto_01": {"id": "loan_auto_01", "type": "Auto Loan", "amount": 800000.00, "status": "Active"}
        }
    },
    {
        "id": "user_456",
        "name": "John Doe",
        "accounts": {
            "acc_savings_03": {
                "account_number": "409000000003",
                "type": "Savings",
                "balance": 5120.50,
                "transactions": [
                    {"id": "txn_4", "desc": "Coffee Shop", "amount": -350.00}
                ],
            }
        },
        "cards": {
            "card_debit_111": {"number": "xxxx-xxxx-xxxx-1111", "type": "Debit", "status": "active"}
        },
        "loans": {}
    },
    {
        "id": "user_789",
        "name": "Priya Singh",
        "accounts": {
            "acc_checking_04": {
                "account_number": "409000000004",
                "type": "Checking",
                "balance": 98000.00,
                "transactions": [
                    {"id": "txn_5", "desc": "Flight Ticket", "amount": -18500.00},
                    {"id": "txn_6", "desc": "Hotel Booking", "amount": -7800.00},
                ]
            }
        },
        "cards": {
            "card_debit_222": {"number": "xxxx-xxxx-xxxx-2222", "type": "Debit", "status": "inactive"},
            "card_credit_333": {"number": "xxxx-xxxx-xxxx-3333", "type": "Credit", "status": "active"}
        },
        "loans": {
            "loan_personal_02": {"id": "loan_personal_02", "type": "Personal Loan", "amount": 50000.00, "status": "Under Review"}
        }
    },
    {
        "id": "user_101",
        "name": "Michael Chen",
        "accounts": {
             "acc_salary_05": {
                "account_number": "409000000005",
                "type": "Salary",
                "balance": 150000.00,
                "transactions": [
                    {"id": "txn_7", "desc": "Monthly Rent", "amount": -25000.00}
                ],
            }
        },
        "cards": {
            "card_corp_444": {"number": "xxxx-xxxx-xxxx-4444", "type": "Corporate Credit", "status": "active"}
        },
        "loans": {
            "loan_home_03": {"id": "loan_home_03", "type": "Home Loan", "amount": 5000000.00, "status": "Paid Off"}
        }
    }
]


def seed_database():
    """Clears the existing collection and inserts all mock user data."""
    print("Connecting to the database...")
    # Clear the collection to avoid duplicate data on re-runs
    users_collection.delete_many({})
    print("Cleared existing user data.")

    # Insert all mock users into the collection
    if mock_users:
        users_collection.insert_many(mock_users)
        print(f"Successfully inserted {len(mock_users)} user documents.")
    else:
        print("No users to insert.")
    
    client.close()
    print("Database connection closed.")


if __name__ == "__main__":
    seed_database()