import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# 初始化状态
if "pitch" not in st.session_state:
    st.session_state.pitch = -5
    st.session_state.trim = -3
    st.session_state.electric_trim = True
    st.session_state.stable = False

def runaway_effect():
    if st.session_state.electric_trim:
        st.session_state.pitch -= 1
        st.session_state.trim -= 1

st.title("✈️ Boeing 737 Runaway Trim Simulator (Non-MAX)")
st.write(
    "You are flying a **Boeing 737 (non-MAX)**. "
    "The aircraft suddenly begins pitching nose-down due to a trim malfunction."
)

st.divider()

# 状态显示
st.subheader("📊 Aircraft Status")
st.metric("Pitch (deg)", st.session_state.pitch)
st.metric("Trim", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)

if st.session_state.pitch >= 0 and not st.session_state.electric_trim:
    st.session_state.stable = True

# 操作区
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Electric Trim ↑"):
        if st.session_state.electric_trim:
            st.session_state.pitch += 1
            st.session_state.trim += 1
        runaway_effect()

with col2:
    if st.button("CUTOUT Trim"):
        st.session_state.electric_trim = False

with col3:
    if st.button("Manual Trim Wheel"):
        if not st.session_state.electric_trim:
            st.session_state.pitch += 2
            st.session_state.trim += 2

# 自动恶化
if not st.session_state.stable:
    runaway_effect()

st.divider()

# 结果显示
if st.session_state.stable:
    st.success("✅ Aircraft stabilized. You regained control.")
else:
    st.warning("⚠️ Aircraft unstable. Choose your actions carefully.")

st.caption(
    "Educational simulation for engineering ethics. "
    "This is not flight training."
)

