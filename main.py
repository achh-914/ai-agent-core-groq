import os
from groq import Groq
from config import GROQ_API_KEY
from tools import get_system_status

# Initialize Groq Client securely
client = Groq(api_key=GROQ_API_KEY or os.environ.get("GROQ_API_KEY"))

def run_agent(prompt: str):
    """
    Executes the AI Agent with the given user prompt.
    """
    print(f"[Input]: {prompt}")
    
    # Example tool integration check
    if "system" in prompt.lower() or "status" in prompt.lower():
        system_info = get_system_status()
        prompt = f"{prompt}\n\n[Context Data]: {system_info}"

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and intelligent AI Assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    output = response.choices[0].message.content
    print(f"[Output]: {output}")
    return output

if __name__ == "__main__":
    print("--- Starting AI Agent ---")
    user_query = "Check system status and give me a quick summary."
    run_agent(user_query)
