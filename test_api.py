"""Test kết nối OpenAI API."""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def test_api():
    try:
        llm = ChatOpenAI(model="gpt-4.1-mini")
        response = llm.invoke("Say hello in Vietnamese")
        print("Kết nối API thành công!")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"Lỗi kết nối API: {e}")
        print("Vui lòng kiểm tra OPENAI_API_KEY trong file .env")


if __name__ == "__main__":
    test_api()
