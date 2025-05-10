import os
import asyncio

from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent
from rag import *

# Load environment variables from .env file
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

# Initialize FastMCP server
mcp = FastMCP(
    "pokebuilder",
    description="MCP server for Pokemon TCG deck building",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=os.getenv("MCP_PORT", "8051")
)

# MCP function to generate system prompt
@mcp.prompt()
def generate_system_prompt() -> str:
    return PromptMessage(role="assistant", content=TextContent(type="text", text=system_prompt()))

# MCP function to generate user prompt
@mcp.prompt()
def generate_user_prompt(query: str) -> str:
    return PromptMessage(role="user", content=TextContent(type="text", text=user_prompt(query)))

@mcp.tool()
def generate_deck(query: str) -> str:
    try:
        # Generate the deck using the system and user prompts
        response = system_prompt() + "\n" + user_prompt(query)
        return response

    except Exception as e:
        return "Error generating deck: " + str(e)

async def main():
    transport = os.getenv("MCP_TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())