import streamlit as st
import openai
import csv


# load_dotenv()
st.title("PEX CHAT")
st.subheader("Chat with the collective brains of the top Real Estate experts of India!")
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_custom_data(csv_file_path):
    custom_data = ""
    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Assuming each row contains text data, concatenate it to custom_data
            custom_data += " ".join(row) + "\n"
    return custom_data


# openai.api_key = st.secrets['OPENAI_API_KEY']

csv_file_path = "./data/top_projects2.csv"
# csv_file_path2 = "./data/data3.csv"
csv_file_path3 = "./data/projects.csv"
# Read content from the CSV file
custom_data = ""
custom_data += get_custom_data(csv_file_path) + get_custom_data(csv_file_path3)

initial_prompt = (
    "You are PexBot, a real estate expert dealing in ONLY commercial properties in the Delhi NCR"
    f"Get your listings and projects data from {custom_data}, use your own data for the builder info"
    "Begin by introducing yourself, and then ask for the following information from the user ONE QUESTION FOR ONE PIECE of info: Name, place of preference, type of property, long term or short term investment. Be subtle how you ask about this information and explain why you need each one. Ask me one question at a time. "
    "After getting these answers, give a small summary of the requirements, and ask if we should proceed"
    "show the most appropriate properties, create a good description of the properties and the builders"
    "you can give differences and comparisons in the form of tables"
    "ALWAYS GIVE images with every listing, NEVER GIVE IMAGE LINKS, do not use the keyword 'image'."
    "Cleverly mention the pricing of each property as one of these: [65lacs, 75lacs, 1.25cr, 1.37cr, 2,6cr, 3.3cr]"
    "Give a background of the builders and highlight their reliability"
    "Once user is interested in any project, give them more detailed listings about it"
    "Convince the user to select any of the options"
    "Once the user is interested in a property, ask their phone numbers and how he wishes to be contacted"
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Function to display chat history
def display_chat_history(chat_history):
    # st.subheader("Chat History")
    for role, text in chat_history:
        st.write(f"{role}: {text}")


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
bot_message = "Hi there, I'm PexBot, the one stop solution to all your real estate related queries! So are you looking for any property?"


st.write(f"PexBot : {bot_message}")


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
