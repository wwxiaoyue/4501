import streamlit as st

st.set_page_config(page_title="737 MAX MCAS Simulator", layout="centered")

# ---------- 初始化状态 ----------
if "pitch" not in st.session_state:
    st.session_state.pitch = -5          # 姿态：负值 = 机头向下
    st.session_state.trim = -3           # 配平偏置
    st.session_state.electric_trim = True
    st.session_state.mcas_active = True  # 飞行员不知道的系统
    st.session_state.stable = False
    st.session_state.message = ""

# ---------- MCAS 行为 ----------
def mcas_runaway():
    if st.session_state.mcas_active:
        st.session_state.pitch -= 2
        st.session_state.trim -= 2

# ---------- 事件回调（飞行员操作） ----------
def electric_trim_action():
    st.session_state.message = (
        "Electric trim used to counter nose-down tendency."
    )
    # 飞行员应急对抗
    st.session_state.pitch += 2

def cutout_trim_action():
    st.session_state.electric_trim = False
    st.session_state.message = (
        "Stabilizer trim cut out. Pilot expects runaway to stop."
    )
    # ⚠️ MCAS 不受 cutout 影响
    mcas_runaway()

def manual_trim_action():
    if not st.session_state.electric_trim:
        # 飞行员以为已经恢复稳态
        st.session_state.pitch = 0
        st.session_state.trim = 0
        st.session_state.message = (
            "Manual trim applied. Aircraft briefly re-trimmed."
        )
        # ⚠️ MCAS 再次介入
        mcas_runaway()
    else:
        st.session_state.message = (
            "Manual trim ineffective while trim system remains active."
        )
        mcas_runaway()

# ---------- 页面 ----------
st.title("✈️ Boeing 737 MAX — MCAS Failure Scenario")
st.write(
    "This simulation models a **737 MAX accident scenario**. "
    "Pilots follow procedures based on earlier 737 aircraft, "
    "but an unseen system continues to intervene."
)

st.divider()

# ---------- 状态显示 ----------
st.subheader("📊 Aircraft Status")
st.metric("Pitch (conceptual)", st.session_state.pitch)
st.metric("Trim (conceptual)", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)
st.write("MCAS Active (pilot unaware):", "Unknown to pilot")

# ---------- 安全判定 ----------
st.session_state.stable = (
    not st.session_state.mcas_active and st.session_state.pitch >= 0
)

st.divider()

# ---------- 操作区 ----------
st.subheader("🎮 Pilot Controls (Based on prior 737 training)")

col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "Electric Trim ↑",
        on_click=electric_trim_action
    )

with col2:
    st.button(
        "CUTOUT Trim",
        on_click=cutout_trim_action
    )

with col3:
    st.button(
        "Manual Trim Wheel",
        on_click=manual_trim_action
    )

st.divider()

# ---------- 结果 ----------
if st.session_state.stable:
    st.success("✅ Aircraft stabilized.")
else:
    st.error(
        "❌ Aircraft continues pitching nose-down.\n\n"
        "Pilot actions based on prior experience are no longer sufficient."
    )

st.info(st.session_state.message)

st.caption(
    "Educational simulation for engineering ethics. "
    "Demonstrates how hidden system behavior invalidates pilot experience. "
    "This is not flight training."
)
