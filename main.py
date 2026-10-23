import os
from groq import Groq

try:
    from config import GROQ_API_KEY
except ImportError:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def chat_loop():
    print("--- 🤖 AI Agent Started (Type 'exit' to quit) ---")
    messages = [
        {"role": "system", "content": "You are a helpful and intelligent AI Assistant."}
    ]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        reply = response.choices[0].message.content
        print(f"\nAI: {reply}")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat_loop()
