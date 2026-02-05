import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# ---------- 初始化 ----------
if "state" not in st.session_state:
    st.session_state.state = {
        "pitch": -5,
        "trim": -3,
        "electric_trim": True,
        "step": 0,
        "stable": False,
        "log": []
    }

def log(msg):
    st.session_state.state["log"].insert(0, msg)

def system_runaway():
    if st.session_state.state["electric_trim"]:
        st.session_state.state["pitch"] -= 1
        st.session_state.state["trim"] -= 1
        return "System: Runaway trim activated (pitch -1)"
    return "System: Runaway stopped"

def check_stable():
    if (
        not st.session_state.state["electric_trim"]
        and st.session_state.state["pitch"] >= -1
    ):
        st.session_state.state["stable"] = True

# ---------- UI ----------
st.title("✈️ Boeing 737 Runaway Trim Simulator (Non-MAX)")
st.write(
    "Each button press represents **one decision step**. "
    "You will immediately see what happened."
)

st.divider()

# 状态区
st.subheader("📊 Aircraft Status")
st.metric("Pitch (deg)", st.session_state.state["pitch"])
st.metric("Trim", st.session_state.state["trim"])
st.write("Electric Trim Active:", st.session_state.state["electric_trim"])
st.write("Step:", st.session_state.state["step"])

st.divider()

# 控制区
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Electric Trim ↑"):
        st.session_state.state["step"] += 1
        log(f"Step {st.session_state.state['step']}: Pilot used Electric Trim (+1 pitch)")
        if st.session_state.state["electric_trim"]:
            st.session_state.state["pitch"] += 1
            st.session_state.state["trim"] += 1
        log(system_runaway())
        check_stable()

with col2:
    if st.button("CUTOUT Trim"):
        st.session_state.state["step"] += 1
        st.session_state.state["electric_trim"] = False
        log(f"Step {st.session_state.state['step']}: Pilot CUT OUT stabilizer trim")
        log("System: Electric trim disabled")
        check_stable()

with col3:
    if st.button("Manual Trim Wheel"):
        st.session_state.state["step"] += 1
        if not st.session_state.state["electric_trim"]:
            st.session_state.state["pitch"] += 2
            st.session_state.state["trim"] += 2
            log(f"Step {st.session_state.state['step']}: Pilot manually trimmed (+2 pitch)")
        else:
            log(f"Step {st.session_state.state['step']}: Manual trim ineffective")
        log(system_runaway())
        check_stable()

st.divider()

# 结果区
if st.session_state.state["stable"]:
    st.success("✅ Aircraft stabilized. You regained control.")
else:
    st.warning("⚠️ Aircraft unstable.")

# 行动日志（即时反馈的关键）
st.subheader("📝 Action Log (Immediate Feedback)")
for entry in st.session_state.state["log"][:8]:
    st.write(entry)

st.caption(
    "Educational simulation for engineering ethics. "
    "Each action produces immediate, visible consequences."
)
