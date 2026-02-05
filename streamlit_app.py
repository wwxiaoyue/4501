import streamlit as st

st.set_page_config(page_title="737 Runaway Trim Simulator", layout="centered")

# ---------- 初始化状态 ----------
if "pitch" not in st.session_state:
    st.session_state.pitch = -5          # 姿态：负值 = 机头向下
    st.session_state.trim = -3           # 配平偏置
    st.session_state.electric_trim = True
    st.session_state.stable = False
    st.session_state.message = ""

def runaway_effect():
    # 只有在 electric trim 仍然开启时，runaway 才会发生
    if st.session_state.electric_trim:
        st.session_state.pitch -= 1
        st.session_state.trim -= 1

# ---------- 页面 ----------
st.title("✈️ Boeing 737 Runaway Trim Simulator (Non-MAX)")
st.write(
    "This is a **conceptual engineering simulation**. "
    "Pitch and trim values represent system trends, not real angles."
)

st.divider()

# ---------- 状态显示 ----------
st.subheader("📊 Aircraft Status")
st.metric("Pitch (conceptual)", st.session_state.pitch)
st.metric("Trim (conceptual)", st.session_state.trim)
st.write("Electric Trim Active:", st.session_state.electric_trim)

# 安全判定（与你之前讨论一致）
if not st.session_state.electric_trim and st.session_state.pitch >= 0:
    st.session_state.stable = True
else:
    st.session_state.stable = False

# ---------- 操作区 ----------
st.subheader("🎮 Pilot Controls")

col1, col2, col3 = st.columns(3)

# ① Electric Trim ↑ —— 临时对抗
with col1:
    if st.button("Electric Trim ↑"):
        st.session_state.message = (
            "Electric trim used to temporarily counter nose-down tendency."
        )
        # 立刻对抗
        st.session_state.pitch += 2


# ② CUTOUT —— 隔离问题源头
with col2:
    if st.button("CUTOUT Trim"):
        st.session_state.electric_trim = False
        st.session_state.message = (
            "Stabilizer trim cut out. Runaway trim is stopped."
        )

# ③ Manual Trim Wheel —— 恢复稳态
with col3:
    if st.button("Manual Trim Wheel"):
        if not st.session_state.electric_trim:
            # 直接恢复到中性稳态
            st.session_state.pitch = 0
            st.session_state.trim = 0
            st.session_state.message = (
                "Manual trim applied. Aircraft re-trimmed to neutral state."
            )
        else:
            st.session_state.message = (
                "Manual trim ineffective while runaway trim is active."
            )

        # 如果还没 cutout，系统仍会继续搞事
        runaway_effect()

st.divider()

# ---------- 结果 ----------
if st.session_state.stable:
    st.success("✅ Aircraft stabilized. Problem resolved.")
else:
    st.warning("⚠️ Aircraft not yet stabilized.")

st.info(st.session_state.message)

st.caption(
    "Educational simulation for engineering ethics. "
    "This is not flight training."
)

