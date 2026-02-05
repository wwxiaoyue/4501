import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# 初始化状态
if "pitch" not in st.session_state:
    st.session_state.pitch = -5
    st.session_state.trim = -3
    st.session_state.electric_trim = True
    st.session_state.stable = False
    st.session_state.message = ""

def system_step():
    # runaway trim happens once per step, only if electric trim is active
    if st.session_state.electric_trim:
        st.session_state.pitch -= 1
        st.session_state.trim -= 1

def check_stable():
    if st.session_state.pitch >= -1 and not st.session_state.electric_trim:
        st.session_state.stable = True

st.title("✈️ Boeing 737 Runaway Trim Simulator (Non-MAX)")
st.write(
    "You are flying a **Boeing 737 (non-MAX)**. "
    "The aircraft begins pitching nose-down due to a trim malfunction."
)

st.divider()

# 状态显示
st.subheader("📊 Aircraft Status")
st.metric("Pitch (deg)", st.session_state.pitch)
st.metric("Trim", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)

st.divider()
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Electric Trim ↑"):
        if st.session_state.electric_trim:
            st.session_state.pitch += 1
            st.session_state.trim += 1
            st.session_state.message = "You countered the trim temporarily."
        else:
            st.session_state.message = "Electric trim is already cut out."
        system_step()

with col2:
    if st.button("CUTOUT Trim"):
        st.session_state.electric_trim = False
        st.session_state.message = "Stabilizer trim cut out. Runaway stopped."
        check_stable()

with col3:
    if st.button("Manual Trim Wheel"):
        if not st.session_state.electric_trim:
            st.session_state.pitch += 2
            st.session_state.trim += 2
            st.session_state.message = "You manually trimmed the aircraft."
            check_stable()
        else:
            st.session_state.message = "Manual trim is ineffective while runaway continues."
        system_step()

st.divider()

# 结果显示
if st.session_state.stable:
    st.success("✅ Aircraft stabilized. You regained control.")
else:
    st.warning("⚠️ Aircraft unstable. Runaway trim may still be active.")

st.info(st.session_state.message)

st.caption(
    "Educational simulation for engineering ethics. "
    "This is not flight training."
)

