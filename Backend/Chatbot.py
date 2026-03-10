from groq import Groq
from json import load, dump
import os
import datetime
from dotenv import dotenv_values
from pathlib import Path

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key
Username = env_vars.get("Username") or os.environ.get("Username") or "User"
Assistantname = env_vars.get("Assistantname") or os.environ.get("Assistantname") or "Jarvis"
GroqAPIKey = env_vars.get("GroqAPIKey") or os.environ.get("GROQ_API_KEY")

# Initialize the Groq client using the provided API key (validate first)
if not GroqAPIKey:
    client = None
else:
    client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages
messages = []

# Resolve chat log path relative to this file so running from different CWDs works
BASE_DIR = Path(__file__).resolve().parent
CHATLOG_PATH = BASE_DIR / "Data" / "ChatLog.json"
CHATLOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Define a system message that provides context to the AI chatbot about its role and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with CHATLOG_PATH.open("r", encoding="utf-8") as f:
        messages = load(f)
except FileNotFoundError:
    with CHATLOG_PATH.open("w", encoding="utf-8") as f:
        dump([], f)

# Function to get real-time date and time information.
def RealtimeInformation():
    current_date_time = datetime.datetime.now()  # Get the current date and time.
    day = current_date_time.strftime("%A")        # Day of the week.
    date = current_date_time.strftime("%d")       # Day of the month.
    month = current_date_time.strftime("%B")      # Full month name.
    year = current_date_time.strftime("%Y")       # Year.
    hour = current_date_time.strftime("%H")       # Hour in 24-hour format.
    minute = current_date_time.strftime("%M")     # Minute.
    second = current_date_time.strftime("%S")     # Second.

    # Format the information into a string.
    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines)  # Join the cleaned lines back together.
    return modified_answer

# Main chatbot function to handle user queries.
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response. """
    # Basic validation
    if client is None:
        return "Error: Groq API key not configured. Set GroqAPIKey in your .env file."

    try:
        # Load the existing chat log from the JSON file.
        with CHATLOG_PATH.open("r", encoding="utf-8") as f:
            messages = load(f)

        # Append the user's query to the messages list.
        messages.append({"role": "user", "content": str(Query)})

        # Make a request to the Groq API for a response.
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        # Process the streamed response chunks.
        for chunk in completion:
            # defensive checks to avoid attribute errors
            try:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)
            except Exception:
                content = None

            if content:
                Answer += content

        Answer = Answer.replace("</s>", "")

        # Append the chatbot's response to the messages list and save log.
        messages.append({"role": "assistant", "content": Answer})
        with CHATLOG_PATH.open("w", encoding="utf-8") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        # Print error and reset chat log without infinite recursion.
        print(f"Error: {e}")
        with CHATLOG_PATH.open("w", encoding="utf-8") as f:
            dump([], f, indent=4)
        return f"Chatbot error: {e}"

# Main program entry point
if __name__ == "__main__":
    print("Welcome to ChatBot! Type 'exit' or 'quit' to end the chat.")
    
    while True:
        try:
            user_input = input("Enter Your Question: ")  # Prompt user
            if user_input.lower() in ["exit", "quit"]:  # Exit condition
                print("Goodbye!")
                break

            response = ChatBot(user_input)  # Call your ChatBot function
            print(response)  # Print the chatbot response

        except Exception as e:
            print(f"Oops! Something went wrong: {e}")

