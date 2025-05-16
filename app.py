import streamlit as st
import os
import logging
from debate_bot import DebateBot
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AI Debate Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Add custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #34495e;
        margin-bottom: 2rem;
        text-align: center;
        font-style: italic;
    }
    
    .user-message {
        background-color: #3498db;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 1rem;
    }
    
    .bot-message {
        background-color: #2c3e50;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 1rem;
    }
    
    .message-container {
        display: flex;
        margin-bottom: 1rem;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #ecf0f1;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
    
    .user-avatar {
        background-color: #3498db;
        color: white;
    }
    
    .bot-avatar {
        background-color: #2c3e50;
        color: white;
    }
    
    .stButton button {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton button:hover {
        background-color: #1a2631;
    }
    
    .style-emoji {
        font-size: 1.3rem;
        margin-right: 0.5rem;
    }
    
    .stRadio > div {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .stRadio label {
        background-color: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    
    .stRadio label:hover {
        background-color: #e9ecef;
    }
    
    .debate-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .info-badge {
        background-color: #2c3e50;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        display: inline-flex;
        align-items: center;
    }
    
    .reset-button {
        background-color: #e74c3c !important;
    }
    
    .reset-button:hover {
        background-color: #c0392b !important;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background-color: #e0e0e0;
    }
    
    footer {
        margin-top: 3rem;
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize the debate bot
debate_bot = DebateBot()

# App title and description
st.markdown('<h1 class="main-title">🤖 AI Debate Bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Engage in thought-provoking debates with a bot that adapts to your style and difficulty preferences</p>', unsafe_allow_html=True)

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    st.session_state.topic = ""
    st.session_state.difficulty = "medium"
    st.session_state.style = "friendly"
    st.session_state.debate_started = False
    st.session_state.is_debate_topic = True

# Sidebar configuration
with st.sidebar:
    st.header("Debate Settings")
    
    if not st.session_state.debate_started:
        # Topic input
        topic = st.text_input("Debate Topic", placeholder="e.g., Climate Change Solutions, AI Ethics...")
        
        # Difficulty selection
        st.subheader("Difficulty Level")
        difficulty_descriptions = {k: v['description'] for k, v in Config.DIFFICULTY_LEVELS.items()}
        difficulty = st.radio(
            "Select difficulty:",
            options=list(difficulty_descriptions.keys()),
            format_func=lambda x: f"{x.capitalize()}: {difficulty_descriptions[x]}",
            index=1,  # Default to medium
            label_visibility="collapsed"
        )
        
        # Style selection
        st.subheader("Conversation Style")
        
        # Create a more visual style selector
        style_options = list(Config.CONVERSATION_STYLES.keys())
        style_cols = st.columns(2)
        
        style_radio_options = []
        for idx, style_name in enumerate(style_options):
            emoji = Config.STYLE_EMOJIS[style_name]
            style_radio_options.append(f"{emoji} {style_name.capitalize()}")
        
        style_idx = st.radio(
            "Select style:",
            options=range(len(style_options)),
            format_func=lambda x: style_radio_options[x],
            index=0,  # Default to friendly
            label_visibility="collapsed"
        )
        style = style_options[style_idx]
        
        # Display style description
        st.info(Config.CONVERSATION_STYLES[style]['description'])
        
        # Start debate button
        if st.button("Start Debate", use_container_width=True):
            if not topic:
                st.error("Please provide a debate topic.")
            else:
                st.session_state.topic = topic
                st.session_state.difficulty = difficulty
                st.session_state.style = style
                st.session_state.debate_started = True
                st.session_state.is_debate_topic = True
                
                # Generate initial message
                initial_message = {
                    "role": "user",
                    "content": f"I'd like to debate about {topic}. Please provide an opening statement."
                }
                
                # Add to conversation history
                st.session_state.conversation.append(initial_message)
                
                # Generate bot response
                bot_response = debate_bot.generate_response(
                    st.session_state.conversation,
                    topic,
                    difficulty,
                    style
                )
                
                # Add bot response to conversation
                bot_message = {
                    "role": "assistant",
                    "content": bot_response
                }
                st.session_state.conversation.append(bot_message)
                st.rerun()
    else:
        # Display current debate info
        st.markdown(f"<div class='debate-info'>", unsafe_allow_html=True)
        st.markdown(f"<strong>Topic:</strong> {st.session_state.topic}", unsafe_allow_html=True)
        
        difficulty_emoji = "🔍" if st.session_state.difficulty == "easy" else "🧠" if st.session_state.difficulty == "medium" else "🔬"
        style_emoji = Config.STYLE_EMOJIS[st.session_state.style]
        
        st.markdown(
            f"<span class='info-badge'>{difficulty_emoji} {st.session_state.difficulty.capitalize()}</span>"
            f"<span class='info-badge'>{style_emoji} {st.session_state.style.capitalize()}</span>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Reset debate button
        if st.button("Reset Debate", use_container_width=True, type="primary", key="reset_btn", help="Start a new debate"):
            st.session_state.conversation = []
            st.session_state.topic = ""
            st.session_state.debate_started = False
            st.rerun()

# Main conversation area
if st.session_state.debate_started:
    # Display conversation history
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="message-container" style="justify-content: flex-end;">
                    <div class="user-message">{message["content"]}</div>
                    <div class="message-avatar user-avatar">👤</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="message-container">
                    <div class="message-avatar bot-avatar">🤖</div>
                    <div class="bot-message">{message["content"]}</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    # Input for user message
    user_message = st.text_area("Your argument:", height=100, placeholder="Type your argument here...", key="user_input")
    
    # Send button
    if st.button("Send Message", use_container_width=True):
        if user_message:
            # Check if it's a debate-related message by analyzing the content
            is_debate_topic = True
            
            # List of debate-unrelated patterns (questions about the bot, general chat, etc.)
            non_debate_patterns = [
                "who are you", "what's your name", "how are you", "tell me about yourself",
                "what can you do", "help me with", "can you help", "tell me a joke",
                "what's the weather", "what time is it", "who made you", "what are you",
                "hello", "hi there", "good morning", "good afternoon", "good evening",
                "tell me about", "explain", "what is", "how does", "why is"
            ]
            
            user_message_lower = user_message.lower()
            for pattern in non_debate_patterns:
                if pattern in user_message_lower and st.session_state.topic not in user_message_lower:
                    is_debate_topic = False
                    break
            
            if is_debate_topic:
                # Add user message to conversation
                st.session_state.conversation.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Show loading spinner while generating response
                with st.spinner("Bot is thinking..."):
                    # Generate bot response
                    bot_response = debate_bot.generate_response(
                        st.session_state.conversation,
                        st.session_state.topic,
                        st.session_state.difficulty,
                        st.session_state.style
                    )
                
                # Add bot response to conversation
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": bot_response
                })
            else:
                # If not a debate-related message, ask for a debate topic
                debate_reminder = f"I'm an AI Debate Bot focused on debating specific topics. We're currently discussing '{st.session_state.topic}'. Please provide an argument related to this topic to continue our debate."
                
                # Add user message to conversation
                st.session_state.conversation.append({
                    "role": "user",
                    "content": user_message
                })
                
                # Add bot response to conversation
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": debate_reminder
                })
            
            # Clear the input
            st.session_state.user_input = ""
            
            # Rerun the app to update the UI
            st.rerun()

# Footer
st.markdown("""
<footer>
    <p>Powered by Mistral AI | AI Debate Bot © 2025</p>
    <p>The bot may occasionally make mistakes or present incorrect information. Always verify important facts.</p>
</footer>
""", unsafe_allow_html=True)

# Check if API key is configured
if not Config.MISTRAL_API_KEY:
    st.sidebar.warning("⚠️ Mistral API key not configured. Set the MISTRAL_API_KEY environment variable to use the bot.")