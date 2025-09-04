from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
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

    model_with_tools = llm.bind_tools(tools)

    tool_node = ToolNode(tools)

    def should_continue(state: MessagesState):
        messages =state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
        
        
    async def call_model(state: MessagesState):
        messages = state["messages"]
        response = await model_with_tools.ainvoke(messages)
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        should_continue,
    )
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    math_response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "what's (10 + 5) x 12?"}]}
    )
    
    return math_response

    
print(asyncio.run(main()))