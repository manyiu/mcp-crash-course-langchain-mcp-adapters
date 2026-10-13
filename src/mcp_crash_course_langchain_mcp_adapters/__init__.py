import asyncio
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), os.getenv("AZURE_TOKEN_PROVIDER")
)

llm = ChatOpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=token_provider,
    model="gpt-5-nano",
    temperature=0,
)

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Volumes/Samsung_990_Pro/Repositories/mcp-crash-course-langchain-mcp-adapters/src/mcp_crash_course_langchain_mcp_adapters/servers/math_server.py"],

)

async def _main() -> None:
    print("Hello from mcp-crash-course-langchain-mcp-adapters!")

    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_agent(llm, tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What's 3 + 5 * 2?")]})
            print(result["messages"][-1].content)


def main() -> None:
    asyncio.run(_main())
