import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from euriai.langchain_llm import EuriaiLangChainLLM

# Load environment variables
load_dotenv()
api_key = os.getenv("EURON_API_TOKEN")

# Page configuration
st.set_page_config(
    page_title="Conversational Playground (Gemini & LLaMA)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

def get_custom_prompt():
    persona = st.session_state.get('selected_persona', 'Default')
    personas = {
        'Default': """You are a helpful AI assistant.\nCurrent conversation:\n{history}\nHuman: {input}\nAI:""",
        'Expert': """You are an expert consultant with deep knowledge across multiple fields.\nPlease provide detailed, technical responses when appropriate.\nCurrent conversation:\n{history}\nHuman: {input}\nExpert:""",
        'Creative': """You are a creative and imaginative AI that thinks outside the box.\nFeel free to use metaphors and analogies in your responses.\nCurrent conversation:\n{history}\nHuman: {input}\nCreative AI:"""
    }
    return PromptTemplate(
        input_variables=["history", "input"],
        template=personas[persona]
    )

def main():
    initialize_session_state()

    with st.sidebar:
        st.title("🛠️ Chat Settings")

        # Model selection
        st.subheader("Model Selection")
        model_name = st.selectbox(
            'Choose your model:',
            ['gemini-2.0-flash', 'llama-4-maverick-17b-128e-instruct'],
            help="Select the Euron model for conversation"
        )

        # Memory setting
        st.subheader("Memory Settings")
        memory_length = st.slider(
            'Conversation Memory (messages)',
            1, 10, 5
        )

        # Persona selector
        st.subheader("AI Persona")
        st.session_state.selected_persona = st.selectbox(
            'Select conversation style:',
            ['Default', 'Expert', 'Creative']
        )

        # Chat stats
        if st.session_state.start_time:
            st.subheader("📊 Chat Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", len(st.session_state.chat_history))
            with col2:
                duration = datetime.now() - st.session_state.start_time
                st.metric("Duration", f"{duration.seconds // 60}m {duration.seconds % 60}s")

        # Clear chat
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.start_time = None
            st.rerun()

    st.title("🤖 Conversational Playground (Gemini & LLaMA)")

    # Initialize memory and model
    memory = ConversationBufferWindowMemory(k=memory_length)
    euron_chat = EuriaiLangChainLLM(
        api_key=api_key,
        model=model_name,
        temperature=0.7
    )

    # Conversation chain
    conversation = ConversationChain(
        llm=euron_chat,
        memory=memory,
        prompt=get_custom_prompt()
    )

    # Load previous conversation into memory
    for message in st.session_state.chat_history:
        memory.save_context(
            {'input': message['human']},
            {'output': message['AI']}
        )

    # Display chat history
    for message in st.session_state.chat_history:
        with st.container():
            st.write("🙂 You")
            st.info(message['human'])
        with st.container():
            st.write(f"🤖 Assistant ({st.session_state.selected_persona} mode)")
            st.success(message['AI'])
        st.write("")

    # Input text area
    st.markdown("### 💭 Your Message")
    user_question = st.text_area(
        "",
        height=100,
        placeholder="Type your message here...",
        key="user_input"
    )

    # Send + Clear buttons
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    with col3:
        if st.button("🔄 New Topic", use_container_width=True):
            memory.clear()
            st.success("Memory cleared for new topic!")

    # Handle sending message
    if send_button and user_question:
        if not st.session_state.start_time:
            st.session_state.start_time = datetime.now()

        with st.spinner('🤔 Thinking...'):
            try:
                response = conversation(user_question)
                message = {
                    'human': user_question,
                    'AI': response['response']
                }
                st.session_state.chat_history.append(message)
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        f"Using Euron API | Persona: {st.session_state.selected_persona.lower()} | Memory: {memory_length} messages"
    )

if __name__ == "__main__":
    main()
