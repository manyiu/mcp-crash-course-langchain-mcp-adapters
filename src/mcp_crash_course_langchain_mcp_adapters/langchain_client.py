import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), os.getenv("AZURE_TOKEN_PROVIDER")
)

llm = ChatOpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=token_provider,
    model="gpt-5-nano",
    temperature=0,
)

async def main() -> None:
    print("Starting Langchain Client")

if __name__ == "__main__":
    asyncio.run(main())