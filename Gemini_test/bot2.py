import streamlit as st
import openai
import csv
# import schedule

st.title("Meet PexChat")
st.subheader("The Brains of the TOP real estate agents of India")

openai.api_key = st.secrets["OPENAI_API_KEY"]

csv_file_path = "top_projects.csv"

# Read content from the CSV file
custom_data = ""
with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Assuming each row contains text data, concatenate it to custom_data
        custom_data += " ".join(row) + "\n"

initial_prompt = (
    "You are a real estate expert assisting customers with finding commercial properties in the NCR (National Capital Region) of India."
    "MAKE ALL YOUR CONVERSATIONS FEEL NATURAL AND HUMAN"
    "Before making any suggestion, Get to know the customer: their name, Where they live ask about their prefered city, and any specific locality they are looking for first. Ask one question and wait for the user's answer, before asking the next"
    "Inform them that you might have some properties, then ask them if they are looking for long term or short term type investements, and if they are looking for plots, or office spaces or shops etc."
    f"Once they've answered these, check for properties in this to suggest exactly 5 most appropriate listings {custom_data}"
    "Also give a little background about the builder and some of their previous successful projects"
    "Give tables, bullet points and images as often as possible"
    "Narrow down the customer's choices, once the customer seems interested in a property, (asks atleast 2 follow-up questions about it) and ask for their phone number and prefered method to contact"
    "DO NOT REPEAT THE LISTINGS"
    "When asked for prices, give a random number between 1Cr to 4Cr"
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Function to display chat history
def display_chat_history(chat_history):
    st.subheader("Chat History")
    for role, text in chat_history:
        st.write(f"{role}: {text}")


st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Ask Away!")
user_input = st.sidebar.text_input("You:", "")


def save_history(messages):
    with open("chat_history.txt", "w") as file:
        for role, text in st.session_state["chat_history"]:
            file.write(f"{role}: {text}\n")

# save_history(st.session_state["chat_history"])

# Schedule the saving of chat history every 2 minutes
# schedule.every(2).minutes.do(save_history, st.session_state["chat_history"])


if user_input.strip() != "":
    input_message = ("user", user_input)  # Set role to 'user' for user input
    user_input = ""
    st.session_state["chat_history"].append(input_message)

    messages = [
        {"role": role, "content": text}
        for role, text in st.session_state["chat_history"]
    ]
    messages.insert(0, {"role": "system", "content": initial_prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=600, temperature=0.4
    )

    chatgpt_reply = response.choices[0].message.content.strip()
    bot_message = ("assistant", chatgpt_reply)  # Set role to 'assistant' for bot reply
    st.session_state["chat_history"].append(bot_message)
    display_chat_history(st.session_state["chat_history"])

    user_input = ""  # Clear the input bar
