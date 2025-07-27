# custom_tool.py
from crewai.tools import BaseTool
from typing import Type, Optional # Import Optional
from pydantic import BaseModel, Field
import requests


class BankingToolInput(BaseModel):
    """Input schema for the BankingTool."""
    method: str = Field(..., description="The HTTP method to use, either 'GET' or 'POST'.")
    endpoint: str = Field(..., description="The specific API endpoint to call. For example: '/get-statement/user_123/acc_savings_01'.")
    # This line is now corrected to allow a dictionary OR None
    payload: Optional[dict] = Field(None, description="The JSON payload required for POST requests. This should be None for GET requests.")


class BankingTool(BaseTool):
    name: str = "Banking API Tool"
    description: str = (
        "A tool to interact with the banking API for all banking operations. "
        "To get a statement, use method='GET' and the endpoint='/get-statement/{user_id}/{account_id}'. "
        "To block a card, use method='POST' and endpoint='/block-card', providing user_id and card_id in the payload. "
        "To apply for a loan, use method='POST' and endpoint='/apply-for-loan', providing user_id, loan_type, and amount in the payload."
    )
    args_schema: Type[BaseModel] = BankingToolInput

    def _run(self, method: str, endpoint: str, payload: Optional[dict] = None) -> str:
        base_url = "http://localhost:8001"
        try:
            if method.upper() == 'GET':
                response = requests.get(f"{base_url}{endpoint}")
            elif method.upper() == 'POST':
                response = requests.post(f"{base_url}{endpoint}", json=payload)
            else:
                return "Error: Invalid HTTP method specified."
            
            response.raise_for_status()
            return str(response.json()) # Return as string for the LLM
        except requests.exceptions.RequestException as e:
            return f"Error interacting with API: {e}"