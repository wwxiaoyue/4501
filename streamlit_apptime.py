import streamlit as st
import time

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# ---------- 初始化状态 ----------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.pitch = -5
    st.session_state.trim = -3
    st.session_state.electric_trim = True
    st.session_state.stable = False
    st.session_state.message = ""
    st.session_state.game_running = False

# ---------- 时间影响参数 ----------
TIME_STEP = 0.5          # 每 0.5 秒更新一次
TRIM_EFFECT_GAIN = 0.2   # trim 对 pitch 的影响强度

# ---------- 系统时间演化 ----------
def time_step_update():
    if st.session_state.game_running:
        if st.session_state.trim < 0:
            # trim 越负，pitch 下降越快
            st.session_state.pitch += TRIM_EFFECT_GAIN * st.session_state.trim

# ---------- 事件回调 ----------
def start_game():
    st.session_state.game_running = True
    st.session_state.message = "Simulation started. Aircraft response evolving over time."

def electric_trim_action():
    st.session_state.message = "Electric trim used to counter nose-down tendency."
    st.session_state.pitch += 2

def cutout_trim_action():
    st.session_state.electric_trim = False
    st.session_state.message = "Stabilizer trim cut out. Runaway trim stopped."

def manual_trim_action():
    if not st.session_state.electric_trim:
        st.session_state.pitch = 0
        st.session_state.trim = 0
        st.session_state.message = "Manual trim applied. Aircraft re-trimmed to neutral."
    else:
        st.session_state.message = "Manual trim ineffective while runaway trim is active."

# ---------- 页面 ----------
st.title("✈️ Boeing 737 Runaway Trim Simulator (Game Mode)")
st.write(
    "This interactive simulation adds **time pressure**. "
    "As long as trim remains negative, pitch will continue to degrade over time."
)

st.divider()

# ---------- 游戏控制 ----------
st.subheader("🕒 Simulation Control")
if not st.session_state.game_running:
    st.button("▶️ Start Simulation", on_click=start_game)
else:
    st.success("Simulation running...")

st.divider()

# ---------- 状态显示 ----------
st.subheader("📊 Aircraft Status")
st.metric("Pitch (conceptual)", round(st.session_state.pitch, 2))
st.metric("Trim (conceptual)", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)

# ---------- 安全判定 ----------
st.session_state.stable = (
    not st.session_state.electric_trim
    and st.session_state.trim == 0
    and st.session_state.pitch >= 0
)

# ---------- 操作区 ----------
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("Electric Trim ↑", on_click=electric_trim_action)

with col2:
    st.button("CUTOUT Trim", on_click=cutout_trim_action)

with col3:
    st.button("Manual Trim Wheel", on_click=manual_trim_action)

st.divider()

# ---------- 结果 ----------
if st.session_state.stable:
    st.success("✅ Aircraft stabilized. You regained control.")
elif st.session_state.pitch < -10:
    st.error("💥 Aircraft lost control. Impact imminent.")
else:
    st.warning("⚠️ Aircraft unstable. Time is critical.")

st.info(st.session_state.message)

st.caption(
    "Educational simulation for engineering ethics. "
    "Demonstrates time-dependent system behavior and pilot workload."
)

# ---------- 时间推进 ----------
time_step_update()

if st.session_state.game_running and not st.session_state.stable:
    time.sleep(TIME_STEP)
    st.experimental_rerun()
