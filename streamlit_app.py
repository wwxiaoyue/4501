import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# ---------- 初始化 ----------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.pitch = -5
    st.session_state.trim = -3
    st.session_state.electric_trim = True
    st.session_state.stable = False
    st.session_state.message = "Aircraft begins to pitch nose-down."
    st.session_state.step = 0


# ---------- 系统逻辑 ----------
def system_runaway():
    if st.session_state.electric_trim:
        st.session_state.pitch -= 1
        st.session_state.trim -= 1


def check_stable():
    if st.session_state.pitch >= -1 and not st.session_state.electric_trim:
        st.session_state.stable = True


def advance_step():
    st.session_state.step += 1
    system_runaway()
    check_stable()


# ---------- UI ----------
st.title("✈️ Boeing 737 Runaway Trim Simulator (Non-MAX)")
st.write(
    "You are flying a **Boeing 737 (non-MAX)**. "
    "A trim malfunction causes the aircraft to pitch nose-down."
)

st.divider()

st.subheader("📊 Aircraft Status")
st.write(f"**Time Step:** {st.session_state.step}")
st.metric("Pitch (deg)", st.session_state.pitch)
st.metric("Trim", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)

st.divider()
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Electric Trim ↑"):
        st.session_state.message = "You counter the trim temporarily."
        if st.session_state.electric_trim:
            st.session_state.pitch += 1
            st.session_state.trim += 1
        advance_step()

with col2:
    if st.button("CUTOUT Trim"):
        st.session_state.electric_trim = False
        st.session_state.message = "Stabilizer trim cut out. Runaway stopped."
        advance_step()

with col3:
    if st.button("Manual Trim Wheel"):
        if not st.session_state.electric_trim:
            st.session_state.pitch += 2
            st.session_state.trim += 2
            st.session_state.message = "You manually trimmed the aircraft."
        else:
            st.session_state.message = "Manual trim ineffective while runaway continues."
        advance_step()

st.divider()

# ---------- 结果 ----------
if st.session_state.stable:
    st.success("✅ Aircraft stabilized. You regained control.")
else:
    st.warning("⚠️ Aircraft unstable. Choose actions carefully.")

st.info(st.session_state.message)

st.caption(
    "Educational simulation for engineering ethics. "
    "This is not flight training."
)

