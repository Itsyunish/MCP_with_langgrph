from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from dotenv import load_dotenv


load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [r"C:\AI\practise_mcp\math_server.py"],
                "transport": 'stdio'
            }
        }
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    tools = await client.get_tools()
    
    agent = create_react_agent(
        llm,
        tools,
    )
    
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is 10 + 5 ?"}]}
    )
    
    for msg in math_response['messages']:
        if getattr(msg, "content", None):
            print(msg.content)

    
asyncio.run(main())