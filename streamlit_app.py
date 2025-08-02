import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# --- Page Configuration ---
st.set_page_config(
    page_title="Sriram's Retail Bot",
    page_icon="🛍️",
    layout="wide"
)
# Title of the app
st.title("🛍️ Sriram's Retail Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# User input prompt
user_input = st.chat_input("Ask about the Retail Domain...")

# Function to check if input is Retail-related
def is_retail_related(text):
    retail_keywords = [
        "retail", "store", "pos", "point of sale", "inventory", "sku",
        "merchandising", "checkout", "sales", "pricing", "discount",
        "barcode", "supply chain", "omnichannel", "ecommerce",
        "retailer", "loyalty", "customer experience", "in-store",
        "footfall", "promotion", "product return", "stock"
    ]
    return any(word in text.lower() for word in retail_keywords)

# Function to get OpenAI response with restriction
def get_response(prompt):
    restricted_prompt = (
        "You are an AI assistant that only answers questions related to the Retail domain. "
        "If the user asks anything unrelated to Retail, politely refuse to answer and ask them to stay on topic.\n\n"
        f"User: {prompt}\n"
        "Assistant:"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Retail domain expert. Only answer Retail-related questions."}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": restricted_prompt}]
    )

    return response.choices[0].message.content

# Process input
if user_input:
    if is_retail_related(user_input):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        assistant_response = get_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        with st.chat_message("assistant"):
            st.markdown("I only discuss the Retail related. Please ask something related to Retail.")
