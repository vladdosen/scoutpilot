import streamlit as st

# Konfiguracija strane
st.set_page_config(page_title="Scout Pilot", layout="wide")

# Session state za posede i poene
if "quarters" not in st.session_state:
    st.session_state.quarters = {
        "Q1": {"posessions": 0, "points": 0},
        "Q2": {"posessions": 0, "points": 0},
        "Q3": {"posessions": 0, "points": 0},
        "Q4": {"posessions": 0, "points": 0},
    }
    st.session_state.current_q = "Q1"
    st.session_state.history = []

# Header
st.title("🏀 Scout Pilot - Tagovanje poseda i poena")
st.markdown("### Test verzija aplikacije za scout analizu")

# Izbor četvrtine
st.session_state.current_q = st.selectbox("Izaberi četvrtinu:", ["Q1", "Q2", "Q3", "Q4"])

# Funkcije za update
def add_possession():
    st.session_state.quarters[st.session_state.current_q]["posessions"] += 1
    st.session_state.history.append(("posession", st.session_state.current_q))

def add_points(points):
    st.session_state.quarters[st.session_state.current_q]["points"] += points
    st.session_state.history.append(("points", st.session_state.current_q, points))

def undo():
    if st.session_state.history:
        last = st.session_state.history.pop()
        if last[0] == "posession":
            st.session_state.quarters[last[1]]["posessions"] -= 1
        elif last[0] == "points":
            st.session_state.quarters[last[1]]["points"] -= last[2]

# Dugmići
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("➕ Posjed"):
        add_possession()
with col2:
    if st.button("➕ 1 Poen"):
        add_points(1)
with col3:
    if st.button("➕ 2 Poena"):
        add_points(2)
with col4:
    if st.button("➕ 3 Poena"):
        add_points(3)
with col5:
    if st.button("↩️ Undo"):
        undo()

st.divider()

# Prikaz rezultata
for q in ["Q1", "Q2", "Q3", "Q4"]:
    data = st.session_state.quarters[q]
    st.subheader(f"📊 {q}")
    st.write(f"• Posedi: {data['posessions']}")
    st.write(f"• Poeni: {data['points']}")
    if data['posessions'] > 0:
        ppp = round(data['points'] / data['posessions'], 2)
        st.write(f"• Poeni po posedu (PPP): {ppp}")
    else:
        st.write("• Poeni po posedu (PPP): -")
