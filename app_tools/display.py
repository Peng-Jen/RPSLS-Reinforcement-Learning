import streamlit as st
from .const import *

def display_intro():
    st.markdown('### 🎮 Introduction to RPSLS Game')
    st.markdown("""
        **Rock-Paper-Scissors-Lizard-Spock** (RPSLS) is an extended version of the classic 'Rock, Paper, Scissors' game.
        The game adds two more moves (Lizard and Spock) to the mix, making it more interesting. Here’s how it works:

        - **Rock** (✊) crushes **Scissors** (✌️) and crushes **Lizard** (🤌)
        - **Paper** (🖐️) covers **Rock** (✊) and disproves **Spock** (🖖)
        - **Scissors** (✌️) cuts **Paper** (🖐️) and decapitates **Lizard** (🤌)
        - **Lizard** (🤌) eats **Paper** (🖐️) and poisons **Spock** (🖖)
        - **Spock** (🖖) smashes **Scissors** (✌️) and vaporizes **Rock** (✊)

        The game proceeds with two players choosing their moves and the winner being determined by a set of rules.
    """)

    st.image('./images/images/rules.png', caption='Rock-Paper-Scissors-Lizard-Spock Rules (https://openclipart.org/detail/325665/rock-paper-scissors-lizard-spock)', use_container_width=True)
    st.markdown("""
        In the context of our simulation, you are playing against an AI agent that has learned the game
        using reinforcement learning. You can choose your move, and the AI will make its decision based on the strategies it has learned.

        Choose an option below and see how well you perform against the AI!
    """)

def display_rewards_table():
    st.markdown('#### 📘 Rewards Table')
    rewards_table = st.session_state.table
    with st.expander('Click to view reward matrix'):
        import pandas as pd
        df = pd.DataFrame(index=actions, columns=actions)
        for a1 in actions:
            for a2 in actions:
                r_ai, r_player = rewards_table[(a1, a2)]
                df.loc[a1, a2] = f'AI: {r_ai}, You: {r_player}'
        st.dataframe(df, use_container_width=True)

def display_single_game(p, a, result):
    col1, col2, *_ = st.columns(5)
    with col1:
        st.markdown(f"""
            <div style='font-size:28px;'>
                <strong>You:</strong> {emoji_map[p]} vs. <strong>AI:</strong> {emoji_map[a]}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style='font-size:28px; color: green;'>
                ✅ You win!
            </div>
        """ if result.startswith('✅') else f"""
            <div style='font-size:28px; color: red;'>
                ❌ You lose!
            </div>
        """ if result.startswith('❌') else f"""
            <div style='font-size:28px; color: gray;'>
                ⚖️ Draw!
            </div>
        """, unsafe_allow_html=True)

def display_stats():
    st.write('')
    st.markdown('#### 📊 Match Summary')
    st.markdown(f'- Your score : **{st.session_state.player_score}** (in {st.session_state.player_wins} wins)')
    st.markdown(f'- AI score: **{st.session_state.ai_score}** (in {st.session_state.ai_wins} wins)')
    st.markdown(f'- Draws: **{st.session_state.draws}**')

def display_history():
    st.markdown('#### 📜 Recent History')
    for i, (p, a, res) in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f'{i}. You: {emoji_map[p]} vs. AI: {emoji_map[a]} → {res}')
