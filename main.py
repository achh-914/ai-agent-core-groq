import os
import datetime
from groq import Groq

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def get_system_status():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"System is fully operational. Current timestamp: {now}"

system_prompt = """
You are an advanced AI Agent specialized in Infrastructure and Cloud. 
Always respond professionally and concisely.
"""

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Check status. Context: {get_system_status()}"}
    ]
)

print("--- AI AGENT RESPONSE ---")
print(response.choices[0].message.content)
