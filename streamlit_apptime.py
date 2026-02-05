import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Game", layout="centered")

# ---------- 初始化 ----------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.pitch = -5.0      # 飞机姿态
    st.session_state.trim = -3.0       # 配平偏置
    st.session_state.electric_trim = True
    st.session_state.turn = 0
    st.session_state.game_over = False
    st.session_state.stable = False
    st.session_state.message = ""

# ---------- 游戏参数 ----------
TRIM_EFFECT_GAIN = 0.3     # trim 对 pitch 的“持续伤害”
GAME_OVER_PITCH = -12.0    # 失败阈值

# ---------- 回合推进逻辑 ----------
def next_turn():
    if st.session_state.game_over or st.session_state.stable:
        return

    st.session_state.turn += 1

    # 回合结算：trim 造成持续影响
    if st.session_state.trim < 0:
        st.session_state.pitch += TRIM_EFFECT_GAIN * st.session_state.trim

    # 失败判定
    if st.session_state.pitch <= GAME_OVER_PITCH:
        st.session_state.game_over = True
        st.session_state.message = "Loss of control. Terrain impact imminent."

# ---------- 飞行员操作 ----------
def electric_trim_action():
    st.session_state.message = "Electric trim used to temporarily counter pitch."
    st.session_state.pitch += 2

def cutout_trim_action():
    st.session_state.electric_trim = False
    st.session_state.message = "Trim system cut out. Runaway stopped."

def manual_trim_action():
    if not st.session_state.electric_trim:
        st.session_state.pitch = 0
        st.session_state.trim = 0
        st.session_state.message = "Manual trim applied. Aircraft re-trimmed."
    else:
        st.session_state.message = "Manual trim ineffective while runaway continues."

# ---------- 页面 ----------
st.title("✈️ Boeing 737 Runaway Trim — Turn-Based Game")

st.write(
    "This is a **turn-based educational game**. Each turn represents time passing. "
    "As long as trim remains negative, the aircraft will continue to pitch down."
)

st.divider()

# ---------- 游戏状态 ----------
st.subheader("🎯 Game Status")
st.write(f"**Turn:** {st.session_state.turn}")

st.metric("Pitch", round(st.session_state.pitch, 2))
st.metric("Trim", round(st.session_state.trim, 2))
st.write("Electric Trim Active:", st.session_state.electric_trim)

# ---------- 危险进度条 ----------
st.subheader("⚠️ Aircraft Stability")
danger = max(0, min(100, int(-st.session_state.pitch * 8)))
st.progress(danger)

# ---------- 胜负判定 ----------
if not st.session_state.electric_trim and st.session_state.trim == 0 and st.session_state.pitch >= 0:
    st.session_state.stable = True

if st.session_state.stable:
    st.success("✅ SUCCESS: Aircraft stabilized.")
elif st.session_state.game_over:
    st.error("💥 GAME OVER: Aircraft lost control.")
else:
    st.warning("⚠️ Aircraft unstable. Choose actions carefully.")

st.info(st.session_state.message)

st.divider()

# ---------- 操作区 ----------
st.subheader("🎮 Pilot Actions (One action per turn)")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("Electric Trim ↑", on_click=electric_trim_action, disabled=st.session_state.game_over)

with col2:
    st.button("CUTOUT Trim", on_click=cutout_trim_action, disabled=st.session_state.game_over)

with col3:
    st.button("Manual Trim Wheel", on_click=manual_trim_action, disabled=st.session_state.game_over)

st.divider()

# ---------- 回合控制 ----------
st.subheader("⏭️ Time Control")

st.button(
    "Next Turn",
    on_click=next_turn,
    disabled=st.session_state.game_over or st.session_state.stable
)

st.caption(
    "Turn-based simulation for engineering ethics. "
    "Demonstrates how risk accumulates over time due to system design."
)
