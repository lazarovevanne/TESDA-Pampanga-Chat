import streamlit as st
import time

# --------------------------
# Simple rule-based chatbot function
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").strip()

    if user_message in ["hi", "hello", "hey", "start"]:
        return "👋 Hello! How can I help you today?"

    elif "Available CBT Programs" in user_message or user_message == "available cbt programs":
    	return '📦 You can See available Community Based-Trainings here: <a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vSFbhD901AR_TCRJ__OcfOBR-I6hBphNo4ai1Djy_e9VPeAYMBba-E8TnPLE91jNeyeewG-VrPdAfns/pubhtml" target="_blank">Available CBT Programs</a>'

    elif "Requirements" in user_message or user_message == "Requirements":
        return "📝 Here are the requirements for the application for Community Based Training."

    elif "talk to agent" in user_message or user_message == "Register":
        return '📝 To Register Kindly click this link:<a href="https://docs.google.com/forms/d/e/1FAIpQLSfMMWs-PyeHqGMyQBp9DvhqCZBZyEkPjKsbUrSk6sut_4OPRw/viewform?usp=dialog" target="_blank">CBT Registration Form</a>'

    else:
        return "❓ Sorry, I didn’t understand that. Please choose an option below or type 'help'."

# --------------------------
# Page config and session
# --------------------------
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    # messages is a list of tuples: (role, text)
    st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Chatbot. Type 'help' to see options.")]

# last_action will hold a quick-action command when a button is clicked
if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Sidebar info + reset
# --------------------------
with st.sidebar:
    st.title("ℹ️ About this Chatbot")
    st.write("This is a simple **rule-based chatbot** built with Streamlit. You can:")
    st.markdown("""
    - 👋 Greet the bot  
    - 📝 Create an account  
    - 📦 View courses  
    - 📞 Talk to a human agent  
    """)
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Chatbot. Type 'help' to see options.")]
        st.session_state.last_action = None
        st.experimental_rerun()

# --------------------------
# Top title
# --------------------------
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Rule-Based Chatbot</h1>", unsafe_allow_html=True)
st.write("Interact with the chatbot by typing or using quick action buttons below.")

# --------------------------
# Quick action buttons (safe pattern)
# --------------------------
col1, col2, col3 = st.columns(3)
if col1.button("📝 Available CBT Programs"):
    st.session_state.last_action = "Available CBT Programs"
if col2.button("📦 Requirements"):
    st.session_state.last_action = "Requirements"
if col3.button("📝 Register"):
    st.session_state.last_action = "Register"

# --------------------------
# Determine user_input:
# - priority: last_action (button) -> chat_input (if available) -> text_input fallback
# --------------------------
user_input = None

# If a button was clicked (last_action set), consume it exactly once
if st.session_state.last_action:
    user_input = st.session_state.last_action
    # clear it immediately so it won't repeat on next run
    st.session_state.last_action = None

# Try to use chat_input (Streamlit >= 1.25). If not available, fall back to text_input.
try:
    # chat_input returns a value only when user submits
    if user_input is None:
        chat_in = st.chat_input("Type your message here...")
        if chat_in:
            user_input = chat_in
except Exception:
    # fallback to text_input with a session_state key so we can clear it after processing
    if user_input is None:
        # use a session key so we can reset it safely
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("Type your message here:", value=st.session_state.typed_value, key="typed_value")
        # Only process if not empty and not same as last processed (to avoid reprocessing)
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("You", typed)):
            user_input = typed

# --------------------------
# Process a single user_input (if any)
# --------------------------
if user_input:
    # Append user message
    st.session_state.messages.append(("You", user_input))

    # Simulate typing effect (non-blocking visual)
    with st.spinner("Bot is typing..."):
        time.sleep(0.9)

    # Get bot reply
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An internal error occurred while generating a reply: {e}"

    st.session_state.messages.append(("Bot", bot_reply))

    # If using the text_input fallback, clear stored value after processing
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display conversation safely
# --------------------------
for entry in st.session_state.messages:
    # defensive check to avoid unpacking errors
    if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
        # skip malformed entries
        continue
    role, msg = entry
    if role == "You":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:15px; margin:5px; text-align:right;'>"
            f"🧑 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin:5px; text-align:left;'>"
            f"🤖 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
