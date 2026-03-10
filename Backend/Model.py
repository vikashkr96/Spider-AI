import cohere
from rich import print
from dotenv import load_dotenv
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()  # loads .env from current directory
cohereAPIKey = os.getenv("CohereAPIKey")

if not cohereAPIKey:
    raise ValueError("CohereAPIKey not found in .env file. Make sure .env exists and has CohereAPIKey=your_key")

# Initialize Cohere client
co = cohere.Client(api_key=cohereAPIKey)

# -----------------------------
# Recognized function prefixes
# -----------------------------
funcs = [
    "exit", "general", "realtime", "open", "close",
    "play", "generate image", "system", "content",
    "google search", "youtube search", "reminder"
]

# -----------------------------
# Preamble instructions
# -----------------------------
preamble = """
You are a very accurate Decision-Making Model.
Your job is to classify the user's query.

DO NOT answer the query.
ONLY classify it into one or more of the following formats:

general (query)
realtime (query)
open (app or website)
close (app or website)
play (song name)
generate image (prompt)
reminder (time date message)
system (task)
content (topic)
google search (topic)
youtube search (topic)
exit

If multiple actions are requested, return them separated by commas.

If unsure, respond with:
general (query)
"""

# -----------------------------
# Chat history (Cohere roles must be uppercase)
# -----------------------------
chatHistory = [
    {"role": "USER", "message": "how are you?"},
    {"role": "CHATBOT", "message": "general how are you?"},
    {"role": "USER", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "CHATBOT", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "USER", "message": "open chrome and firefox"},
    {"role": "CHATBOT", "message": "open chrome, open firefox"},
    {"role": "USER", "message": "set a reminder at 9pm tomorrow"},
    {"role": "CHATBOT", "message": "reminder 9pm tomorrow"}
]

# -----------------------------
# Decision-making function
# -----------------------------
def FirstLayerDMM(prompt: str):
    """
    Classifies a query into tasks like 'general', 'open', 'reminder', etc.
    Returns a list of recognized intents.
    """
    stream = co.chat_stream(
    model="command-xlarge-nightly", 
    message=prompt,
    temperature=0.3,
    chat_history=chatHistory,
    prompt_truncation="OFF",
    preamble=preamble
)


    response_text = ""
    for event in stream:
        if event.event_type == "text-generation":
            response_text += event.text

    # Clean and split response
    response_text = response_text.replace("\n", "").lower()
    tasks = [t.strip() for t in response_text.split(",")]

    # Filter valid tasks
    final_tasks = []
    for task in tasks:
        for func in funcs:
            if task.startswith(func):
                final_tasks.append(task)
                break

    # Fallback
    if not final_tasks:
        final_tasks.append(f"general {prompt}")

    return final_tasks

# -----------------------------
# Run interactive loop
# -----------------------------
if __name__ == "__main__":
    print("[bold green]Jarvis Decision Model Ready[/bold green]")
    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue

        result = FirstLayerDMM(user_input)
        print(result)

        if any(r.startswith("exit") for r in result):
            print("[bold red]Exiting...[/bold red]")
            break
