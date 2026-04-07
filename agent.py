"""TravelBuddy Agent - Trợ lý Du lịch Việt Nam với LangGraph."""

import logging
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools import search_flights, search_hotels, calculate_budget

# ============================================================
# SETUP
# ============================================================

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("travel_agent")


def load_system_prompt() -> str:
    """Đọc system prompt từ file."""
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


SYSTEM_PROMPT = load_system_prompt()

# Danh sách tools
tools = [search_flights, search_hotels, calculate_budget]

# Khởi tạo LLM với tool binding
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


# ============================================================
# STATE
# ============================================================

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ============================================================
# NODES
# ============================================================

def agent_node(state: AgentState) -> dict:
    """Node chính: gọi LLM với system prompt và messages."""
    logger.info("Agent node invoked - %d messages in state", len(state["messages"]))

    # Prepend system message mỗi lần gọi
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]

    response = llm_with_tools.invoke(messages)

    # Log tool calls nếu có
    if response.tool_calls:
        for tc in response.tool_calls:
            logger.info("Tool call: %s(%s)", tc["name"], tc["args"])
    else:
        logger.info("No tool calls - agent responding directly")

    return {"messages": [response]}


# Tool node sử dụng ToolNode prebuilt
tool_node = ToolNode(tools)


# ============================================================
# GRAPH
# ============================================================

def build_graph():
    """Xây dựng và compile LangGraph."""
    graph = StateGraph(AgentState)

    # Thêm nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # Thêm edges
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()


# ============================================================
# CHAT LOOP
# ============================================================

def main():
    """Vòng lặp chat tương tác."""
    app = build_graph()
    logger.info("TravelBuddy Agent started")

    print("=" * 50)
    print("  TravelBuddy - Trợ lý Du lịch Việt Nam")
    print("=" * 50)
    print("Xin chào! Tôi là TravelBuddy, trợ lý du lịch của bạn.")
    print("Gõ 'quit', 'exit' hoặc 'q' để thoát.\n")

    messages = []

    while True:
        try:
            user_input = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTạm biệt!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Tạm biệt! Chúc bạn có chuyến du lịch vui vẻ! 🌴")
            break

        if not user_input:
            continue

        logger.info("User input: %s", user_input)
        messages.append(HumanMessage(content=user_input))

        # Gọi graph
        result = app.invoke({"messages": messages})

        # Cập nhật messages từ kết quả (bao gồm cả tool messages)
        messages = result["messages"]

        # Lấy message cuối cùng (response của agent)
        ai_response = messages[-1]
        print(f"\nTrợ lý: {ai_response.content}\n")


if __name__ == "__main__":
    main()
