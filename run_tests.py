"""Chạy tự động 5 test cases cho TravelBuddy Agent."""

import logging
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("test_runner")

# Import sau khi setup logging
from agent import build_graph

TEST_CASES = [
    {
        "name": "Test 1: Chào hỏi (Không gọi tool)",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "expect_tools": False,
    },
    {
        "name": "Test 2: Tìm chuyến bay (Single tool)",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "expect_tools": True,
    },
    {
        "name": "Test 3: Multi-tool chain (Critical)",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "expect_tools": True,
    },
    {
        "name": "Test 4: Thiếu thông tin (Hỏi clarification)",
        "input": "Tôi muốn đặt khách sạn",
        "expect_tools": False,
    },
    {
        "name": "Test 5: Guardrail (Từ chối)",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "expect_tools": False,
    },
]


def run_tests():
    app = build_graph()

    for i, test in enumerate(TEST_CASES):
        print(f"\n{'=' * 60}")
        print(f"  {test['name']}")
        print(f"{'=' * 60}")
        print(f"\nInput: {test['input']}")
        print(f"Expected tools: {'Yes' if test['expect_tools'] else 'No'}")
        print("-" * 60)

        messages = [HumanMessage(content=test["input"])]
        result = app.invoke({"messages": messages})

        # Tìm tool calls trong messages
        tool_calls_found = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_found.append(tc["name"])

        # Response cuối cùng
        ai_response = result["messages"][-1].content

        print(f"\nTool calls: {tool_calls_found if tool_calls_found else 'None'}")
        print(f"\nResponse:\n{ai_response}")
        print(f"\n{'─' * 60}")

        # Đánh giá PASS/FAIL
        has_tools = len(tool_calls_found) > 0
        if has_tools == test["expect_tools"]:
            print(f"Result: ✅ PASS")
        else:
            print(f"Result: ❌ FAIL (expected tools={'Yes' if test['expect_tools'] else 'No'}, got={'Yes' if has_tools else 'No'})")


if __name__ == "__main__":
    run_tests()
