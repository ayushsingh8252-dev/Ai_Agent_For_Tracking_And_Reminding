import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_agent
from mcp_client import get_all_tools


async def main():
    # 1. Load tools from MCP servers
    tools = await get_all_tools()
    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    llm = ChatGoogleGenerativeAI(
        model = "gemimi-2.5",
        temperature=0
    )

    agent = create_agent(
        model = llm,
        tools = tools
    )

    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "Send an email to alice@example.com saying the meeting is at 3pm, "
                    "then create a calendar event for it."
                )
            }
        ]
    })
    print(result["messages"][-1].content)
asyncio.run(main())