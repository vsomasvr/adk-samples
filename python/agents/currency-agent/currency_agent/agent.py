import logging
import os
import uvicorn
import google.auth.transport.requests
import google.oauth2.id_token

from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

load_dotenv()

SYSTEM_INSTRUCTION = (
    "You are a specialized assistant for currency conversions. "
    "Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates. "
    "If the user asks about anything other than currency conversion or exchange rates, "
    "politely state that you cannot help with that topic and can only assist with currency-related queries. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
)

logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
logger.info("--- 🤖 Creating ADK Currency Agent... ---")

# 1. Pre-calculate static values outside the callback for performance
_MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
_AUDIENCE = _MCP_URL.split('/mcp/')[0]
_AUTH_REQUEST = google.auth.transport.requests.Request()

def get_auth_headers(_=None) -> dict[str, str]:

    try:
        id_token = google.oauth2.id_token.fetch_id_token(_AUTH_REQUEST, _AUDIENCE)
        
        logger.info("--- 🔧 MCP Auth: Token refreshed ---")
        return {"Authorization": f"Bearer {id_token}"}
        
    except Exception as e:
        logger.error(f"--- ❌ MCP Auth Error: Failed to fetch token: {e} ---")
        return {}

# Usage remains the same
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(url=_MCP_URL),
    header_provider=get_auth_headers 
)

root_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="currency_agent",
    description="An agent that can help with currency conversions",
    instruction=SYSTEM_INSTRUCTION,
    tools=[mcp_tools],
)

# Make the agent A2A-compatible
# a2a_app = to_a2a(root_agent, port=10000)

