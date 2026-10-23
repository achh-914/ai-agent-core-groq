import os
from groq import Groq
from config import GROQ_API_KEY, DEFAULT_MODEL
from tools import get_system_status, calculate_expression

api_key = GROQ_API_KEY or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def chat_loop():
    print("--- 🤖 AI Agent Started (Type 'exit' to quit) ---")
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent AI Agent. You can provide system status or perform math calculations when asked."
        }
    ]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if "status" in user_input.lower():
            status = get_system_status()
            print(f"\n[Tool Execution]: {status}")
            user_input += f"\n[System Data]: {status}"

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages
        )

        reply = response.choices[0].message.content
        print(f"\nAI: {reply}")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat_loop()
