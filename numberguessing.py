import random
import streamlit as st

def computerchoicefunc():
    computerchoice = random.randint(1, 10)
    return computerchoice

def main():
    # Page configuration
    st.set_page_config(
        page_title="Number Guessing Game",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f0f4f8;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .title-text {
            text-align: center;
            color: #2c3e50;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle-text {
            text-align: center;
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        .info-box {
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 20px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="title-text">🎯 Number Guessing Game</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Can you guess the number I\'m thinking of?</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'computer_choice' not in st.session_state:
        st.session_state.computer_choice = computerchoicefunc()
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.feedback_messages = []
    
    # Game info
    st.markdown("""
        <div class="info-box">
            <strong>📋 Game Rules:</strong><br>
            • I'm thinking of a number between 1 and 10<br>
            • You have 3 attempts to guess it<br>
            • I'll give you hints after each guess
        </div>
    """, unsafe_allow_html=True)
    
    # Display attempts remaining
    attempts_remaining = 3 - st.session_state.attempts
    col1, col2, col3 = st.columns(3)
    with col2:
        st.metric(label="Attempts Remaining", value=attempts_remaining)
    
    st.divider()
    
    # Number input
    st.subheader("Make Your Guess:")
    user_choice = st.slider(
        "Select a number between 1 and 10:",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="guess_slider"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        guess_button = st.button("🎲 Submit Guess", key="guess_btn")
    with col2:
        reset_button = st.button("🔄 New Game", key="reset_btn")
    
    # Handle button clicks
    if reset_button:
        st.session_state.computer_choice = computerchoicefunc()
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.feedback_messages = []
        st.rerun()
    
    if guess_button and not st.session_state.game_over:
        st.session_state.attempts += 1
        
        if user_choice < st.session_state.computer_choice:
            message = f"❌ Guess #{st.session_state.attempts}: Your guess is **LOW**. Try predicting a **higher** number!"
            st.session_state.feedback_messages.append(message)
        elif user_choice > st.session_state.computer_choice:
            message = f"❌ Guess #{st.session_state.attempts}: Your guess is **HIGH**. Try predicting a **lower** number!"
            st.session_state.feedback_messages.append(message)
        else:
            message = f"🎉 **CORRECT!** You guessed it right in **{st.session_state.attempts}** attempt(s)!"
            st.session_state.feedback_messages.append(message)
            st.session_state.game_over = True
        
        # Check if out of attempts
        if st.session_state.attempts >= 3 and user_choice != st.session_state.computer_choice:
            st.session_state.feedback_messages.append(f"😢 Game Over! The number was **{st.session_state.computer_choice}**")
            st.session_state.game_over = True
        
        st.rerun()
    
    # Display feedback messages
    if st.session_state.feedback_messages:
        st.divider()
        st.subheader("Game Feedback:")
        for msg in st.session_state.feedback_messages:
            if "CORRECT" in msg:
                st.markdown(f'<div class="success-box">{msg}</div>', unsafe_allow_html=True)
            elif "Game Over" in msg:
                st.markdown(f'<div class="warning-box">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-box">{msg}</div>', unsafe_allow_html=True)
    
    # Display game status
    if st.session_state.game_over:
        st.divider()
        if st.session_state.feedback_messages[-1].startswith("🎉"):
            st.balloons()
        st.info("Click the 'New Game' button to play again!")

if __name__ == "__main__":
    main()