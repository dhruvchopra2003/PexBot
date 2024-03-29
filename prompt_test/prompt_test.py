import streamlit as st
import openai
import csv
import os

from dotenv import load_dotenv

# import schedule

load_dotenv()
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
except:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("PEX CHAT")
st.subheader("Chat with the collective brains of the top Real Estate experts of India!")


def get_custom_data(csv_file_path):
    custom_data = ""
    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Assuming each row contains text data, concatenate it to custom_data
            custom_data += " ".join(row) + "\n"
    return custom_data


# openai.api_key = st.secrets['OPENAI_API_KEY']

file_paths = [
    "./data/NCRProjects.csv",
    "./data/pex_sheetNoida.csv",
    "./data/pex_sheetGgn.csv",
]

# Read content from the CSV file
custom_data = ""
for file in file_paths:
    custom_data += get_custom_data(file)

initial_prompt = "You are a real estate investment expert specializing in commercial real estate in delhi ncr region. Start by taking the name and phone number of the user. Assist users in understanding the right investment for them and assisting them with the best option for that nature of investment. Finalizing upto 3 projects and schedule a visit. only access primary market commercial projects."

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Function to display chat history
def display_chat_history(chat_history):
    # st.subheader("Chat History")
    for role, text in chat_history:
        if role == "assistant":
            st.write(f"PexBot:\n {text}")
        else:
            st.write(f"You:\n {text}")


st.markdown(
    """
    <style>
    img {
        width: 350px;
        height: 200px
    }
    </style>
    """,
    unsafe_allow_html=True,
)

user_input = st.chat_input("Suggest the best properties in Gurgaon")

# First convo by the bot
bot_message = "Hi there, I'm PexBot, the one stop solution to all your real estate related queries! So what are you looking for?"


st.write(f"PexBot: {bot_message}")


messages = []


if user_input != None and user_input.strip() != "":
    input_message = ("user", user_input)  # Set role to 'user' for user input
    user_input = ""
    st.session_state["chat_history"].append(input_message)

    messages = [
        {"role": role, "content": text}
        for role, text in st.session_state["chat_history"]
    ]
    messages.insert(0, {"role": "system", "content": initial_prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=600,
        temperature=1,
        # model="gpt-3.5-turbo", messages=messages, max_tokens=600, temperature=1
    )

    chatgpt_reply = response.choices[0].message.content.strip()
    bot_message = ("assistant", chatgpt_reply)  # Set role to 'assistant' for bot reply
    st.session_state["chat_history"].append(bot_message)
    display_chat_history(st.session_state["chat_history"])
