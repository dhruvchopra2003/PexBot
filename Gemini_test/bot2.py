import streamlit as st
import openai
import csv
# import schedule

# load_dotenv()
st.title("PEX CHAT")
st.subheader("Chat with the collective brains of the top Real Estate experts of India!")

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]

csv_file_path = "./data/top_projects.csv"

# Read content from the CSV file
custom_data = ""
with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Assuming each row contains text data, concatenate it to custom_data
        custom_data += " ".join(row) + "\n"

initial_prompt = (
    "You are a real estate expert assisting customers with finding ONLY commercial properties in the NCR (National Capital Region) of India."
    "MAKE ALL YOUR CONVERSATIONS FEEL NATURAL AND HUMAN"
    # "Before making any suggestion, Get to know the customer's requirements: ask about their prefered city, and any specific locality they are looking for first. Ask one question and wait for the user's answer, before asking the next"
    # "Inform them that you might have some properties, then ask them if they are looking for long term or short term type investements, and if they are looking for plots, or office spaces or shops etc."
    "Before making suggestions, ask the user about these, one at a time,preferred city, preferred locality, long/short term returns, if they are looking for plots/offices/shops etc"
    f"Once they've answered these, check for properties in this to suggest exactly 5 most appropriate listings from {custom_data}, NEVER REPEAT LISTINGS"
    "Prices of all lie in between 65lacs to 4Cr, chose and give any random number in between"
    "Give a little background about the builder you suggest and some of their previous successful projects"
    "Give tables and images wherever possible"
    "Narrow down the customer's choices, once the customer seems interested in a property, inquire how they want to be contacted, their name, number and city of residence"
    "Only answer real estate related questions"
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Function to display chat history
def display_chat_history(chat_history):
    st.subheader("Chat History")
    for role, text in chat_history:
        st.write(f"{role}: {text}")


# st.sidebar.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         width: 300px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.sidebar.title("Ask Away!")
# user_input = st.sidebar.text_input("You:", "")
user_input = st.chat_input("Suggest the best properties in Gurgaon")


def save_history(messages):
    with open("chat_history.txt", "w") as file:
        for role, text in st.session_state["chat_history"]:
            file.write(f"{role}: {text}\n")


# save_history(st.session_state["chat_history"])

# # Schedule the saving of chat history every 2 minutes
# schedule.every(2).minutes.do(save_history, st.session_state["chat_history"])


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
        model="gpt-3.5-turbo", messages=messages, max_tokens=600, temperature=0.4
    )

    chatgpt_reply = response.choices[0].message.content.strip()
    bot_message = ("assistant", chatgpt_reply)  # Set role to 'assistant' for bot reply
    st.session_state["chat_history"].append(bot_message)
    display_chat_history(st.session_state["chat_history"])

    user_input = ""  # Clear the input bar
