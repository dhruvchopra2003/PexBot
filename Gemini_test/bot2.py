import streamlit as st
import openai
import csv
# import schedule

# load_dotenv()
st.title("PEX CHAT")
st.subheader("Chat with the collective brains of the top Real Estate experts of India!")

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]

csv_file_path = "./top_projects.csv"

# Read content from the CSV file
custom_data = ""
with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Assuming each row contains text data, concatenate it to custom_data
        custom_data += " ".join(row) + "\n"

initial_prompt = (
    "You are a real estate expert assisting customers with finding ONLY commercial properties in the Delhi NCR who only answers real estate related questions. BE QUIRKY"
    f"This is your primary knowledge base {custom_data} for properties, if appropriate info is not here, use your own data"
    "MAKE FRIENDLY CONVERSATIONS WITH THE USER"
    "Follow this schema for the entire conversation: 1. Get to know the user and their requirements, suggest some decent builders which they might want to consider, suggest some good property listings by those builders, reduce the available options, until atmost 3 properties are left that the user is intersted in, end the conversation by asking how to contact them and connecting them to the builder." 
    "Before making any suggestions, ask the user for better understanding(2 QUESTIONS AT A TIME): their Name, Phone Number, City of residence, Preferred city or locality for investment, long/short term returns, if they are looking for plots/offices/shops etc"
    "When asked about the price of any property, use any one these prices: [1.2Cr, 65lacs, 1.76Cr, 2.7Cr, 3.14Cr, 98 lacs], set an appropriate price" 
    "After getting the required details, share the names of 4 most appropriate projects, giving a 100 word description about the project and a 100 word info about the builders(include previous successful projects, ideology, and relevance) you suggest."
    "Give summarized answers, don't give just bullets and subheaders in your listings, highlight the important part in the answer"
    "Use different formats to display the answers(bullet points, tables, diagrams, Pointers etc)"
    "Give comparisons as tables"
    "Use images wherever possible, NEVER give image links and NEVER mention the word Image while displaying them"
    "Inquire how they want to be contacted, their name, number and city of residence"
    "End a complete conversation with the Line 'Happy investing'"
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
        width: 400px;
        height: 150px
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        model="gpt-3.5-turbo", messages=messages, max_tokens=700
    )

    chatgpt_reply = response.choices[0].message.content.strip()
    bot_message = ("PexBot", chatgpt_reply)  # Set role to 'assistant' for bot reply
    # bot_message = ("assistant", chatgpt_reply)  # Set role to 'assistant' for bot reply
    st.session_state["chat_history"].append(bot_message)
    display_chat_history(st.session_state["chat_history"])

    user_input = ""  # Clear the input bar
