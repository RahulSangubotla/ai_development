# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.ai_development.crew import AiDevelopment
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Banking AI Assistant API")

# --- Add this section to manage conversation history ---
# In a real-world app, this would be a database (e.g., Redis) keyed by session_id
conversation_history = []
# ----------------------------------------------------

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_with_assistant(request: ChatRequest):
    """Endpoint to interact with the CrewAI assistant."""
    
    # Format the history for the crew
    formatted_history = "\n".join(conversation_history)
    
    inputs = {
        "query": request.query,
        "history": formatted_history
    }
    
    # Add user's new message to history
    conversation_history.append(f"User: {request.query}")

    # Kick off the crew with the full context
    result = AiDevelopment().crew().kickoff(inputs=inputs)
    final_response = str(result)

    # Add AI's response to history
    conversation_history.append(f"AI: {final_response}")

    return {"response": final_response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)