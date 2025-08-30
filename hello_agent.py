# import os
# import asyncio
# from dotenv import load_dotenv, find_dotenv
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# _: bool = load_dotenv(find_dotenv())

# # ONLY FOR TRACING
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# # 1. Which LLM Service?
# external_client: AsyncOpenAI = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# # 2. Which LLM Model?
# llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )



# async def main():
#     params_config = MCPServerStreamableHttpParams(url="http://localhost:8000/mcp")

#     async with MCPServerStreamableHttp(params=params_config, name="SharedStandAloneMCPServer") as mcp_hello_server:

#         base_agent: Agent = Agent(
#             name="GreetingAgent",
#             instructions="You are a helpful assistant.",
#             model=llm_model,
#             mcp_servers=[mcp_hello_server]
#         )
#     res = await Runner.run(base_agent, "What's can you do in AI world?")
#     print(res.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())

import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams

# Load environment variables
_: bool = load_dotenv(find_dotenv())

# Ensure API keys are available
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in environment.")

# 1. LLM Client
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. LLM Model
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

async def main():
    params_config = MCPServerStreamableHttpParams(url="http://localhost:8000/mcp")

    async with MCPServerStreamableHttp(params=params_config, name="SharedStandAloneMCPServer") as mcp_server:

        # Connect before using in the Agent
        await mcp_server.connect()
        print("✅ Connected to MCP Server")

        # # (Optional) Check tools
        # tools = await mcp_server.list_tools()
        # print(f"🛠️ Tools from MCP server: {tools}")

        # Define the Agent
        base_agent: Agent = Agent(
            name="GreetingAgent",
            instructions="You are a helpful assistant.",
            model=llm_model,
            mcp_servers=[mcp_server],
        )

        res = await Runner.run(base_agent, "What can you do for me today according to my mood?")

        print("Final Output here:\n", res.final_output)

if __name__ == "__main__":
    asyncio.run(main())
