import os
import uvicorn

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
)

# --- 5. Execution ---
if __name__ == "__main__":
    # Cloud Run/Standard deployment port logic
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 Starting ADK Agent on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
