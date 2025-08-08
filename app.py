import streamlit as st

st.set_page_config(page_title="Scout Pilot", layout="wide")

if "possessions" not in st.session_state:
    st.session_state.possessions = []
    st.session_state.current_possession = {}
    st.session_state.lineup = []
    st.session_state.quarter = "Q1"
    st.session_state.game_id = 1

st.title("🏀 Scout Pilot - Game Tagging")

# Game and quarter
st.sidebar.header("Game Info")
st.session_state.game_id = st.sidebar.number_input("Game ID", value=st.session_state.game_id, min_value=1)
st.session_state.quarter = st.sidebar.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], index=["Q1", "Q2", "Q3", "Q4"].index(st.session_state.quarter))

# Lineup
with st.sidebar.expander("🧍‍♂️ Current Lineup (5 players)", expanded=True):
    for i in range(5):
        if len(st.session_state.lineup) < 5:
            st.session_state.lineup.append("")
        st.session_state.lineup[i] = st.text_input(f"Player {i+1}", value=st.session_state.lineup[i], key=f"player_{i}")

# Start or end possession
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Possession"):
        st.session_state.current_possession = {
            "game_id": st.session_state.game_id,
            "quarter": st.session_state.quarter,
            "lineup": list(st.session_state.lineup),
            "offense": "",
            "finish": "",
            "defense": "",
            "paint_touch": False,
            "off_reb_players": 0,
            "off_reb_success": None,
            "points": 0
        }

with col2:
    if st.button("⛔ End Possession"):
        if st.session_state.current_possession:
            st.session_state.possessions.append(st.session_state.current_possession)
            st.success("Possession saved!")
            st.session_state.current_possession = {}

if st.session_state.current_possession:
    st.markdown("### 📝 Tag Current Possession")

    st.session_state.current_possession["offense"] = st.selectbox("Offensive Set", ["", "Delay", "Chin", "2 Down", "Iverson", "Spain", "Horns", "Stagger", "PNR", "Early Offense", "SLOB", "BLOB"], index=0)
    st.session_state.current_possession["finish"] = st.selectbox("Finish Type", ["", "PNR", "Cut", "3pt", "Drive", "Post", "Off Screen", "Transition", "FT"], index=0)
    st.session_state.current_possession["defense"] = st.selectbox("Opponent Defense", ["", "Drop", "Switch", "ICE", "Hedge", "Zone", "Man"], index=0)
    st.session_state.current_possession["paint_touch"] = st.checkbox("Paint Touch?")
    
    st.session_state.current_possession["off_reb_players"] = st.slider("How many players went to offensive rebound?", 0, 5, 0)
    st.session_state.current_possession["off_reb_success"] = st.radio("Did we get the offensive rebound?", [None, "Yes", "No"], index=0, horizontal=True)
    
    st.session_state.current_possession["points"] = st.slider("Points scored in this possession", 0, 4, 0)

st.divider()

# Data table
st.subheader("📊 Tagged Possessions")
if st.session_state.possessions:
    import pandas as pd
    df = pd.DataFrame(st.session_state.possessions)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "scout_data.csv", "text/csv")
else:
    st.info("No possessions logged yet.")
