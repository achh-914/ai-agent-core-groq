import json
from groq import Groq
from config import GROQ_API_KEY, DEFAULT_MODEL
from tools import get_system_status, calculate_expression

client = Groq(api_key=GROQ_API_KEY)

# L'catalogue: kan3arfo l'chef chnou l'adawat li 3ndo
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_status",
            "description": "Get the OS info and current time of this machine",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_expression",
            "description": "Evaluate a basic math expression like (2+3)*4",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
]

AVAILABLE = {
    "get_system_status": get_system_status,
    "calculate_expression": calculate_expression,
}

SYSTEM_PROMPT = (
    "You are an AI agent running in a terminal. "
    "This is a learning project built by a developer who is learning to build AI agents. "
    "Your tools are: get_system_status and calculate_expression. "
    "You have no memory of past projects or any work outside this conversation. "
    "Never invent experiences or facts about yourself. "
    "If you do not know something, say you do not know. "
    "ALWAYS use the calculator tool for any math, never calculate yourself. "
    "Reply in plain text only, no markdown, no tables, max 5 lines."
)


def chat_loop():
    print("--- 🤖 AI Agent Started (Type 'exit' to quit) ---")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        # L'boucle dyal agent
        while True:
            resp = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
                tools=TOOLS,
                max_tokens=1000,
            )
            msg = resp.choices[0].message
            messages.append(msg)

            # L'chef ma bghach adat -> jawab nihai
            if not msg.tool_calls:
                print(f"\nAI: {msg.content}")
                break

            # L'chef tlb adat -> kan-nfdhoha
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments or "{}")
                print(f"🔧 Agent khtar: {call.function.name}({args})")
                result = AVAILABLE[call.function.name](**args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result),
                    }
                )


if __name__ == "__main__":
    chat_loop()
