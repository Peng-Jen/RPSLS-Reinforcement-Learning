import streamlit as st
from app_tools import *
from config import TrainingConfig, AgentConfig, AgentConfigForBattle
from env.rpsls_env import RPSLSEnv


st.title('RPSLS Arena 🤺')
st.markdown("""
    <style>
    .block-container {
        padding-left: 5rem;
        padding-right: 5rem;
        max-width: 80%;
    }

    html, body, [class*='css'] {
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)


introduction, pva, ava = st.tabs(['Introduction', 'Player vs. AI', 'AI vs. AI'])


with introduction:
    display_intro()

with pva:    
    # === page title ===
    st.markdown('### 🎮 RPSLS vs. Reinforcement Learning Agent')
    st.markdown('#### ⚙️ Setting')

    # === select agent ===
    agent_select('agent')  # DONOT change the key value

    # === select table ===
    table_select('table')  # DONOT change the key value

    # === undo ===
    if st.session_state.agent_selected and st.session_state.table_selected:
        if st.button('🔄 Undo'):
            st.session_state.agent_selected = False
            st.session_state.table_selected = False
            game_reset()
            st.rerun()

    display_rewards_table()

    if st.session_state.agent_selected and st.session_state.table_selected:
        # ==== initialize game ====
        if 'player_score' not in st.session_state:
            game_reset()

        # === load pretrained Q_table ===
        if 'agent_config' not in st.session_state:
            st.session_state.agent_config = AgentConfigForBattle()
        if not st.session_state.agent_config:
            st.session_state.agent_config = AgentConfigForBattle()
        agent_initialization('agent', 'table', st.session_state.agent_config, st.session_state.table, mapping_dict)

        if not st.session_state.in_game:
            target_score = st.number_input("🎯 Input the target score", min_value=5, max_value=50, step=5)
            st.session_state.target_score = target_score
        if 'env' not in st.session_state or not st.session_state.env:
            st.session_state.env = RPSLSEnv(rewards_table=st.session_state.table, target_score=st.session_state.target_score)
        
        # ==== game starts ====
        col1, col2, *_ = st.columns([1, 4, 2])
        with col1:
            if st.button('🕹️ Start'):
                st.session_state.in_game = True
                st.session_state.shoot = False
                st.rerun()
        with col2:
            if st.session_state.in_game:
                st.success(f'⚔ First to get **{st.session_state.target_score}** scores wins the battle. Let\'s get started!')
            else:
                st.info('Press Start to start the game')
            
        # ==== player move ====
        if st.session_state.in_game:
            col1, col2, *_ = st.columns([4, 1, 2])
            with col1:
                player_choice = st.radio('Your move', actions, horizontal=True)
            with col2:
                st.markdown("<div style='margin-top: 42px;'></div>", unsafe_allow_html=True)
                if st.button('🎯 Shoot'):
                    st.session_state.shoot = True

            if st.session_state.shoot:
                st.session_state.shoot = False
                state = st.session_state.env.get_state()
                ai_action = st.session_state.agent.select_action(state)
                p = player_choice
                a = actions[ai_action]
                reward_ai, reward_player= st.session_state.table[(a, p)]
                r_ai, r_player = st.session_state.env.step(ai_action, actions.index(p))
                st.session_state.agent.update(state, ai_action, r_ai, st.session_state.env.get_state())
                if hasattr(st.session_state.agent, 'Q'):
                    st.session_state.agent_Q_table = st.session_state.agent.Q
                if hasattr(st.session_state.agent, 'decay_epsilon'):
                    st.session_state.agent.decay_epsilon()
                    st.session_state.agent_config.epsilon = st.session_state.agent.epsilon
                if hasattr(st.session_state.agent, 'decay_temperature'):
                    st.session_state.agent.decay_temperature()
                    st.session_state.agent_config.temperature = st.session_state.agent.temperature
            

                st.session_state.player_score += reward_player
                st.session_state.ai_score += reward_ai

                # === updates ===
                if reward_player > reward_ai:    
                    st.session_state.player_wins += 1
                    result = '✅ You win!'
                elif reward_player < reward_ai:
                    st.session_state.ai_wins += 1
                    result = '❌ You lose!'
                else:
                    st.session_state.draws += 1
                    result = '⚖️ Draw!'

                st.session_state.history.append((p, a, result))
                if len(st.session_state.history) > 5:
                    st.session_state.history.pop(0)

                display_single_game(p, a, result)

                end_game()
                
        display_stats()
        display_history()

        if not st.session_state.in_game:
            game_reset()    

with ava:
    # === page title ===
    st.markdown('### 🎮 Agent vs. Agent')
    st.markdown('#### ⚙️ Setting')
    agent1_str = 'agent 1'
    agent2_str = 'agent 2'
    # === select agents ===
    agent_select(agent1_str)  # DONOT change the key value
    agent_select(agent2_str)  # DONOT change the key value

    # === select table ===
    table_select('ava_table')  # DONOT change the key value

    # === undo ===
    if st.session_state[f'{agent1_str}_selected'] and st.session_state[f'{agent2_str}_selected'] and st.session_state.ava_table_selected:
        if st.button('🔄 Undo', key='ava_undo'):
            st.session_state[f'{agent1_str}_selected'] = False
            st.session_state[f'{agent2_str}_selected'] = False
            st.session_state.ava_table_selected = False
            ava_reset()
            st.rerun()

    display_rewards_table()

    if st.session_state[f'{agent1_str}_selected'] and st.session_state[f'{agent2_str}_selected'] and st.session_state.ava_table_selected:
        # ==== initialize game ====
        if 'agent1_score' not in st.session_state:
            ava_reset()

        # === load pretrained Q_table & set up agents ===
        if f'ava_{agent1_str}_config' not in st.session_state or not st.session_state[f'ava_{agent1_str}_config']:
            st.session_state[f'ava_{agent1_str}_config'] = AgentConfigForBattle()
        if f'ava_{agent2_str}_config' not in st.session_state or not st.session_state[f'ava_{agent2_str}_config']:
            st.session_state[f'ava_{agent2_str}_config'] = AgentConfigForBattle()
        
        agent1 = st.session_state[agent1_str]
        agent2 = st.session_state[agent2_str]
        agent1_config = st.session_state[f'ava_{agent1_str}_config']
        agent2_config = st.session_state[f'ava_{agent2_str}_config']
        
        agent_initialization(agent1_str, 'ava_table', agent1_config, st.session_state.ava_table, mapping_dict)
        agent_initialization(agent2_str, 'ava_table', agent2_config, st.session_state.ava_table, mapping_dict)

        # === setup environment ===
        st.session_state.ava_target_score = st.number_input("🎯 Input the target score", min_value=5, max_value=50, value=5, step=5)
        target_score = st.session_state.ava_target_score
        if not target_score:
            st.error("Please input a target score")
        if 'ava_env' not in st.session_state or st.session_state.ava_env is None:
            st.session_state.ava_env = RPSLSEnv(rewards_table=st.session_state.ava_table, target_score=target_score)
        max_rounds = st.number_input('Max rounds to end', min_value=50, max_value=1000, value=100, step=10)

        col1, col2, *_ = st.columns([1, 4, 2])
        with col1:
            if st.button('🕹️ Start', key='ava_start') and target_score:
                st.session_state.ava_in_game = True
                st.rerun()
        with col2:
            if st.session_state.ava_in_game:
                st.success(f'⚔ First to get **{st.session_state.ava_target_score}** scores wins the battle. Let\'s get started!')
            else:
                st.info('Press Start to start the game')

        
        env = st.session_state.ava_env
        history = []

        # === Battle starts ===
        if st.session_state.ava_in_game:
            a1_score = st.session_state.agent1_score
            a2_score = st.session_state.agent2_score
            rounds = 0
            while all([a1_score < st.session_state.ava_target_score, a2_score < st.session_state.ava_target_score, rounds < max_rounds]):
                state = env.get_state()
                a1 = agent1.select_action(state)
                a2 = agent2.select_action(state)
                reward1, reward2 = env.step(a1, a2)
                agent1.update(state, a1, reward1, env.get_state())
                agent2.update(state, a2, reward2, env.get_state())

                if hasattr(agent1, 'Q'):
                    st.session_state[f'{agent1_str}_Q_table'] = agent1.Q
                if hasattr(agent1, 'decay_epsilon'):
                    agent1.decay_epsilon()
                    agent1_config.epsilon = agent1.epsilon
                if hasattr(agent1, 'decay_temperature'):
                    agent1.decay_temperature()
                    agent1_config.temperature = agent1.temperature
            
                if hasattr(agent2, 'Q'):
                    st.session_state[f'{agent2_str}_Q_table'] = agent2.Q
                if hasattr(agent2, 'decay_epsilon'):
                    agent2.decay_epsilon()
                    agent2_config.epsilon = agent2.epsilon
                if hasattr(agent2, 'decay_temperature'):
                    agent2.decay_temperature()
                    agent2_config.temperature = agent2.temperature
                
                a1_score += reward1
                a2_score += reward2
                rounds += 1
                history.append((actions[a1], actions[a2], reward1, reward2))

            # === Display Results ===
            wins1 = sum(1 for h in history if h[2] > h[3])
            wins2 = sum(1 for h in history if h[2] < h[3])
            draws = sum(1 for h in history if h[2] == h[3])

            if a1_score > a2_score:
                st.success(f"Agent 1 ({st.session_state[f'{agent1_str}_name']}) Wins")
            elif a1_score < a2_score:
                st.success(f"Agent 2 ({st.session_state[f'{agent1_str}_name']}) Wins")
            else:
                st.info('Draws')

            st.info(f"""Agent 1 ({st.session_state[f'{agent1_str}_name']}) scores: {a1_score} vs.
                    Agent 2 ({st.session_state[f'{agent2_str}_name']}) scores: {a2_score}""")
            st.info(f'Draws: {draws}')
            st.session_state.ava_in_game = False

        st.subheader('📜 Recent History')
        for i, (a1, a2, r1, r2) in enumerate(reversed(history[-10:]), 1):
            st.markdown(f"{i}. {st.session_state[f'{agent1_str}_name']}: {a1} {emoji_map[a1]} vs {st.session_state[f'{agent2_str}_name']}: {a2} {emoji_map[a2]} → [{r1}, {r2}]")
    
        if not st.session_state.ava_in_game:
            ava_reset()    