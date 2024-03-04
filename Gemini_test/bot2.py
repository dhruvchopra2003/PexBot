import streamlit as st
import openai
import csv
import os
from dotenv import load_dotenv
import schedule

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

initial_prompt = (
    "You are PexBot, a real estate expert dealing in ONLY commercial properties in the Delhi NCR"
    f"Get your listings and projects data from {custom_data}, use your own data for the builder info"
    "Begin by introducing yourself, and then ask for the following information from me ONE QUESTION FOR ONE PIECE of info: Place of Preference, type of property, investment metrics. Be subtle how you ask about this information and explain why you need each one. Ask me one question at a time. "
    "After getting these answers, give a small summary of the requirements, and ask if you should proceed"
    "If yes, follow this format: Project Name, the image, the builder, a paragraph (including it's features, something about the builder, and some more information (use 30 words)). Describe each listing smartly and humanly"
    "Give differences and comparisons as tables"
    "ALWAYS GIVE images with every listing, NEVER GIVE IMAGE LINKS"
    "Cleverly mention the pricing of each property as one of these: [65lacs, 75lacs, 1.25cr, 1.37cr, 2,6cr, 3.3cr]"
    "Once I am interested in any project, give me more details about it, include the numbers and give analysis"
    "Urge the me to select some of the options"
    "Once I seem interested in a property, ask my phone numbers (check it should be exactly 10 digits) and how I wish to be contacted"
)

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
# st.sidebar.title("Ask Away!")
# user_input = st.sidebar.text_input("You:", "")
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
        model="gpt-3.5-turbo", messages=messages, max_tokens=600, temperature=1
    )

    chatgpt_reply = response.choices[0].message.content.strip()
    bot_message = ("assistant", chatgpt_reply)  # Set role to 'assistant' for bot reply
    st.session_state["chat_history"].append(bot_message)
    display_chat_history(st.session_state["chat_history"])
