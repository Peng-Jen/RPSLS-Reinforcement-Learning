import streamlit as st
from .const import *

def agent_select(key):
    radio_key = f"{key}_radio"
    button_key = f"{key}_button"
    selected_key = f"{key}_selected"
    agent_name_key = f"{key}_name"

    if key not in st.session_state:
            st.session_state[key] = None
            st.session_state[selected_key] = False
    if not st.session_state.get(selected_key, False):
        agent_name = st.radio('Choose an agent:', agents, horizontal=True, key=radio_key)
        st.session_state[agent_name_key] = agent_name

        col1, col2, *_ = st.columns([1, 2, 3])
        with col1:
            if st.button('Select Agent', key=button_key):
                st.session_state[selected_key] = True
                st.rerun()
        with col2:
            if not st.session_state.get(selected_key, False):
                st.info('Please choose an agent')
    else:
        col1, _ = st.columns(2)
        with col1:
            st.success(f'✅ {key.capitalize()} is selected ({st.session_state[agent_name_key]})')

def table_select(key):
    radio_key = f"{key}_radio"
    button_key = f"{key}_button"
    selected_key = f"{key}_selected"
    table_name_key = f"{key}_name"

    if key not in st.session_state:
        st.session_state[key] = None
        st.session_state[selected_key] = False

    if not st.session_state[key] or not st.session_state[selected_key]:    
        table = st.radio('Choose rewards table: ', tables, horizontal=True, key=radio_key)
        st.session_state[table_name_key] = table
        st.session_state[key] = tables_map[table]
        col1, col2, *_ = st.columns([1, 2, 3])
        with col1:
            if st.button('Select Table', key=button_key):
                st.session_state[selected_key] = True
                st.rerun()
        with col2:
            if not st.session_state[selected_key]:
                st.info('Please choose a table')
    else:
        col1, _ = st.columns(2)
        with col1:
            st.success(f'✅ Table is selected ({st.session_state[table_name_key]})')


def agent_initialization(agent, table, agent_config):
    import pickle
    name_key = f'{agent}_name'
    table_name_key = f'{table}_name'
    Q_table_key = f'{agent}_Q_table'

    if st.session_state[name_key] in pretrained_agent:
        pretrained_path = f'./saved_Q_tables/{st.session_state[name_key]}_{st.session_state[table_name_key]}.pkl'
        if Q_table_key not in st.session_state:
            with open(pretrained_path, 'rb') as file:
                pretrained = pickle.load(file)
            st.session_state[agent] = agents_map[st.session_state[name_key]](agent_config, pretrained=pretrained)
            st.session_state[Q_table_key] = st.session_state[agent].Q
        else:
            st.session_state[agent] = agents_map[st.session_state[name_key]](agent_config, pretrained=st.session_state[Q_table_key])
    elif st.session_state[agent] is None:
            st.session_state[agent] = agents_map[st.session_state[name_key]](agent_config)

def game_reset():
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draws = 0
    st.session_state.player_wins = 0
    st.session_state.ai_wins = 0
    st.session_state.history = []
    st.session_state.in_game = False
    st.session_state.target_score = None
    st.session_state.env = None
    st.session_state.agent_config = None

def ava_reset():
    st.session_state.agent1_score = 0
    st.session_state.agent2_score = 0
    st.session_state.draws = 0
    st.session_state.agent1_wins = 0
    st.session_state.agent2_wins = 0
    st.session_state.history = []
    st.session_state.ava_in_game = False
    st.session_state.ava_target_score = None
    st.session_state.ava_env = None

def end_game():
    col1, col2, *_ = st.columns([3, 1, 1])
    with col1:
        # === if AI and player simultaneously reach the goal, AI wins ===
        if st.session_state.ai_score >= st.session_state.target_score:
            st.error("💀 AI reached the target score! You lost the game.")
            st.session_state.in_game = False
        elif st.session_state.player_score >= st.session_state.target_score:
            st.success("🏆 You reached the target score! You win the game!")
            st.session_state.in_game = False
    if not st.session_state.in_game:
        with col2:
            st.markdown("<div style='margin-bottom: 2px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 New Game"):
                game_reset()
                