"""
🕊️ The Comforter - LangChain + Streamlit
A beautiful web application that provides spiritual encouragement through Bible verses
using LangChain for intelligent responses and Streamlit for the user interface.
"""
import streamlit as st
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from prompts import BIBLE_MOTIVATE_PROMPT, get_prompt_for_context, DATING_ADVICE_PROMPT, SPIRITUAL_GUIDANCE_PROMPT
from utils import VerseManager, extract_keywords_from_input

# Page configuration
st.set_page_config(
    page_title="🕊️ The Comforter - Find Peace in God's Word",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Beautiful custom CSS
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Chat messages */
    .user-message {
        background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border-left: 6px solid #1b5e20;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        position: relative;
    }
    
    .user-message strong {
        color: #c8e6c9;
        font-weight: 600;
    }
    
    .user-message::before {
        content: "💬";
        position: absolute;
        top: -5px;
        left: 15px;
        background: #1b5e20;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border-left: 6px solid #2e003e;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
        position: relative;
    }
    
    .bot-message strong {
        color: #e1bee7;
        font-weight: 600;
    }
    
    .bot-message::before {
        content: "🕊️";
        position: absolute;
        top: -5px;
        left: 15px;
        background: #2e003e;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    .dating-message {
        background: linear-gradient(135deg, #ad1457 0%, #c2185b 100%);
        border-left-color: #880e4f;
        color: white;
    }
    
    .dating-message::before {
        content: "💕";
        background: #880e4f;
    }
    
    .spiritual-message {
        background: linear-gradient(135deg, #283593 0%, #303f9f 100%);
        border-left-color: #1a237e;
        color: white;
    }
    
    .spiritual-message::before {
        content: "✨";
        background: #1a237e;
    }
    
    .programmer-message {
        background: linear-gradient(135deg, #00695c 0%, #00796b 100%);
        border-left-color: #004d40;
        color: white;
    }
    
    .programmer-message::before {
        content: "💻";
        background: #004d40;
    }
    
    .verse-highlight {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1.5rem 0;
        font-style: italic;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.1);
    }
    
    .verse-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #5d4037;
        margin-bottom: 0.5rem;
    }
    
    .verse-reference {
        font-weight: bold;
        color: #bf360c;
        font-size: 0.95rem;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    /* Welcome section */
    .welcome-section {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        border: 2px solid #4caf50;
    }
    
    .example-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Input styling */
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

class ComforterApp:
    """Beautiful LangChain-powered Bible Comforter with Streamlit GUI."""
    
    def __init__(self):
        self.verse_manager = VerseManager()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'api_key_configured' not in st.session_state:
            st.session_state.api_key_configured = False
        if 'current_mode' not in st.session_state:
            st.session_state.current_mode = "general"
        if 'llm' not in st.session_state:
            st.session_state.llm = None
        if 'total_encouragements' not in st.session_state:
            st.session_state.total_encouragements = 0
    
    def setup_api_key(self):
        """Handle OpenAI API key configuration with beautiful UI."""
        st.sidebar.markdown("### 🔑 LangChain + OpenAI Setup")
        
        # Check for API key in secrets or environment
        api_key = None
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
        except Exception:
            # Secrets not available, try environment
            pass
        
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != "test_key_for_now":
            st.session_state.api_key_configured = True
            try:
                if not st.session_state.llm:
                    # Initialize LangChain ChatOpenAI for OpenRouter
                    if "sk-or-v1" in api_key:
                        # OpenRouter configuration
                        st.session_state.llm = ChatOpenAI(
                            temperature=0.7,
                            model="openai/gpt-3.5-turbo",
                            api_key=api_key,
                            base_url="https://openrouter.ai/api/v1",
                            max_tokens=300
                        )
                    else:
                        # Standard OpenAI configuration
                        st.session_state.llm = ChatOpenAI(
                            temperature=0.7,
                            model="gpt-3.5-turbo",
                            api_key=api_key,
                            max_tokens=300
                        )
                st.sidebar.success("✅ LangChain AI Ready!")
                st.sidebar.info("🤖 Using GPT-3.5-turbo for intelligent Bible-based responses")
            except Exception as e:
                st.sidebar.error(f"❌ LangChain setup error: {str(e)}")
                st.session_state.api_key_configured = False
        else:
            st.session_state.api_key_configured = False
            st.sidebar.warning("⚠️ AI features disabled")
            st.sidebar.info("💡 Add your OpenAI API key to enable intelligent responses")
            
            with st.sidebar.expander("🔧 Setup Instructions", expanded=True):
                st.markdown("""
                **For Streamlit Cloud Deployment:**
                1. Go to your app settings in Streamlit Cloud
                2. Navigate to "Secrets" section
                3. Add: `OPENAI_API_KEY = "sk-your-key-here"`
                
                **For Local Development:**
                ```bash
                export OPENAI_API_KEY="sk-your-key-here"
                ```
                
                **Get Your API Key:**
                🔗 [OpenAI Platform](https://platform.openai.com/api-keys)
                
                **Note:** Without API key, you'll get pre-written encouraging responses with Bible verses.
                """)
    
    def render_sidebar(self):
        """Render the sidebar with controls and information."""
        st.sidebar.markdown("# 🕊️ The Comforter")
        st.sidebar.markdown("*Find peace through God's word*")
        
        # API Key setup
        self.setup_api_key()
        
        # Mode selection
        st.sidebar.markdown("### 📋 Support Mode")
        mode = st.sidebar.radio(
            "Choose your context:",
            ["General Life Support", "Relationship & Dating", "Developer Support", "Spiritual Guidance"],
            help="Choose the area where you need encouragement and advice"
        )
        
        mode_mapping = {
            "General Life Support": "general",
            "Relationship & Dating": "dating", 
            "Developer Support": "programmer",
            "Spiritual Guidance": "spiritual"
        }
        st.session_state.current_mode = mode_mapping[mode]
        
        # Quick actions
        st.sidebar.markdown("### ⚡ Quick Actions")
        
        if st.sidebar.button("🎲 Random Verse", help="Get a random encouraging Bible verse"):
            self.show_random_verse()
        
        if st.sidebar.button("🗑️ Clear Chat", help="Clear conversation history"):
            st.session_state.messages = []
            st.rerun()
        
        # Statistics
        st.sidebar.markdown("### 📊 Session Stats")
        st.sidebar.info(f"""
        **Messages:** {len(st.session_state.messages)}
        **Mode:** {mode}
        **Verses Available:** {len(self.verse_manager._verses)}
        """)
        
        # Help section
        with st.sidebar.expander("❓ How to Use"):
            st.markdown("""
            **Getting Started:**
            1. Configure your OpenAI API key above
            2. Choose your support mode
            3. Share what's on your heart
            
            **Examples:**
            - "I'm feeling anxious about tomorrow"
            - "I'm stuck on a coding problem"
            - "I need strength for today"
            - "I'm feeling overwhelmed"
            
            **Features:**
            - AI-powered responses with Bible verses
            - Smart verse selection based on your input
            - Fallback responses when offline
            - Developer-specific encouragement
            """)
    
    def show_random_verse(self):
        """Display a random Bible verse."""
        verse = self.verse_manager.pick_verse()
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Here's an encouraging verse for you:\n\n*\"{verse['text']}\"*\n\n**{verse['ref']}**",
            "type": "verse"
        })
        st.rerun()
    
    def get_ai_response(self, user_input: str) -> str:
        """Generate AI response with verse using LangChain."""
        try:
            # Extract keywords for better verse matching
            keywords = extract_keywords_from_input(user_input)
            
            # Add mode-specific keywords for better verse selection
            if st.session_state.current_mode == "dating":
                keywords.extend(['love', 'wisdom', 'patience', 'guidance'])
            elif st.session_state.current_mode == "spiritual":
                keywords.extend(['faith', 'hope', 'trust', 'guidance'])
            elif st.session_state.current_mode == "programmer":
                keywords.extend(['strength', 'patience', 'wisdom'])
            
            verse = self.verse_manager.pick_verse(keywords=keywords)
            
            # Get appropriate prompt based on mode
            prompt = get_prompt_for_context(st.session_state.current_mode)
            
            # Generate response using LangChain
            chain = prompt | st.session_state.llm
            response = chain.invoke({
                'user_input': user_input,
                'verse_ref': verse['ref'],
                'verse_text': verse['text']
            })
            
            return response.content.strip()
            
        except Exception as e:
            # Fallback response
            return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input: str) -> str:
        """Get fallback response when AI is unavailable."""
        keywords = extract_keywords_from_input(user_input)
        verse = self.verse_manager.pick_verse(keywords=keywords)
        
        # Mode-specific encouraging responses
        if st.session_state.current_mode == "dating":
            if any(word in user_input.lower() for word in ['relationship', 'dating', 'love', 'crush', 'boyfriend', 'girlfriend']):
                response = "Relationships can be both beautiful and challenging. Remember that God has a perfect plan for your love life, and His timing is always best."
            else:
                response = "I understand you're seeking guidance in matters of the heart. Trust that God sees your desires and will guide you to the right person at the right time."
        elif st.session_state.current_mode == "spiritual":
            if any(word in keywords for word in ['faith', 'doubt', 'prayer', 'god']):
                response = "Your spiritual journey is precious to God. It's okay to have questions and doubts - they often lead to deeper faith and understanding."
            else:
                response = "I can sense you're seeking spiritual guidance. Remember that God is always near, ready to listen and guide you through His word."
        elif st.session_state.current_mode == "programmer":
            response = "Every developer faces challenges like this. Take a step back, breathe, and remember that growth comes through overcoming obstacles. Even the best programmers started as beginners."
        elif any(word in keywords for word in ['anxiety', 'anxious', 'worried']):
            response = "I understand how anxiety can feel overwhelming. Remember that you're not alone in this, and it's okay to take things one step at a time."
        elif any(word in keywords for word in ['strength', 'weak', 'tired']):
            response = "When we feel weak, that's when God's strength shines through us most clearly. Your struggles don't define you - your perseverance does."
        elif any(word in keywords for word in ['fear', 'scared', 'afraid']):
            response = "Fear is natural, but you don't have to face it alone. God is with you, and He will give you the courage you need."
        else:
            response = "I hear you, and I want you to know that you're not alone in this journey. Whatever you're facing, there's hope and help available."
        
        return f"{response}\n\n*\"{verse['text']}\"*\n\n**{verse['ref']}**\n\nTake heart and remember that God is with you in every challenge."
    
    def render_chat_interface(self):
        """Render the main chat interface."""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🕊️ The Comforter</h1>
            <p>Find peace and encouragement through God's word</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Apply mode-specific styling for bot messages
                mode_class = ""
                if st.session_state.current_mode == "dating":
                    mode_class = " dating-message"
                elif st.session_state.current_mode == "spiritual":
                    mode_class = " spiritual-message"
                elif st.session_state.current_mode == "programmer":
                    mode_class = " programmer-message"
                
                st.markdown(f"""
                <div class="bot-message{mode_class}">
                    <strong>🕊️ Comfort:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        if st.session_state.current_mode == "programmer":
            placeholder = "Describe your coding challenge or technical struggle..."
        else:
            placeholder = "Share what's on your heart..."
        
        user_input = st.chat_input(placeholder)
        
        if user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user", 
                "content": user_input
            })
            
            # Generate response
            with st.spinner("🕊️ Bringing you comfort..."):
                if st.session_state.api_key_configured and st.session_state.llm:
                    response = self.get_ai_response(user_input)
                else:
                    response = self.get_fallback_response(user_input)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            st.session_state.total_encouragements += 1
            st.rerun()
        
        # Welcome message for new users
        if not st.session_state.messages:
            st.markdown("""
            ### Welcome to The Comforter! 🕊️
            
            I'm here to provide peace and encouragement through God's word. Whether you're facing:
            
            - **Life challenges** - anxiety, loneliness, discouragement, fear
            - **Coding struggles** - bugs, imposter syndrome, technical frustrations  
            - **Spiritual questions** - doubt, seeking guidance, need for strength
            - **Daily stress** - work pressure, relationships, uncertainty
            
            Share what's on your heart, and receive personalized comfort with relevant Bible verses.
            
            **Choose your support mode in the sidebar and start the conversation below.** ⬇️
            """)
            
            # Show example verses
            st.markdown("### 📖 Comforting Bible Verses")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="verse-highlight">
                    <div class="verse-text">
                        <strong>For Peace:</strong><br>
                        "Peace I leave with you, my peace I give unto you: not as the world giveth, give I unto you."
                    </div>
                    <div class="verse-reference">- John 14:27</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="verse-highlight">
                    <div class="verse-text">
                        <strong>For Comfort:</strong><br>
                        "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit."
                    </div>
                    <div class="verse-reference">- Psalm 34:18</div>
                </div>
                """, unsafe_allow_html=True)
    
    def run(self):
        """Run the Streamlit application."""
        self.render_sidebar()
        self.render_chat_interface()

def main():
    """Main application entry point."""
    app = ComforterApp()
    app.run()

if __name__ == "__main__":
    main()