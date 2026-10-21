import time
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="과목별 타이머 & 스톱워치", page_icon="⏱️", layout="centered")

# ----------------------------------------------------
# 1. 세션 상태 초기화 (총 공부 시간 및 과목별 누적 시간)
# ----------------------------------------------------
# 과목별 누적 학습 시간 (초 단위)
if "subject_study_time" not in st.session_state:
    st.session_state.subject_study_time = {
        "국어": 0,
        "수학": 0,
        "영어": 0,
        "탐구": 0,
        "기타": 0
    }

# 스톱워치 세션 상태
if "stopwatch_running" not in st.session_state:
    st.session_state.stopwatch_running = False
if "stopwatch_time" not in st.session_state:
    st.session_state.stopwatch_time = 0

# 타이머 세션 상태
if "timer_active" not in st.session_state:
    st.session_state.timer_active = False
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# ----------------------------------------------------
# 2. 상단 레이아웃 (제목 & 우측 상단 총 공부 시간)
# ----------------------------------------------------
col_title, col_total = st.columns([1.5, 1])

# 총 공부 시간 계산 (모든 과목 누적 시간의 합)
total_seconds = sum(st.session_state.subject_study_time.values())
t_mins, t_secs = divmod(total_seconds, 60)
t_hours, t_mins = divmod(t_mins, 60)

with col_title:
    st.title("⏱️ 과목별 타이머")

with col_total:
    # 우측 상단에 총 공부 시간 박스 표시
    st.markdown(
        f"""
        <div style="background-color: #f0f2f6; padding: 12px; border-radius: 10px; text-align: center; margin-top: 10px;">
            <span style="font-size: 0.85em; color: #555; font-weight: bold;">🔥 오늘 총 공부 시간</span><br>
            <span style="font-size: 1.6em; font-weight: bold; color: #2E86AB;">{t_hours:02d}:{t_mins:02d}:{t_secs:02d}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ----------------------------------------------------
# 3. 과목 선택 및 과목별 현재 공부 시간 출력
# ----------------------------------------------------
subject = st.selectbox("과목을 선택하세요", ["국어", "수학", "영어", "탐구", "기타"])

# 현재 선택된 과목의 누적 학습 시간
sub_secs = st.session_state.subject_study_time[subject]
s_m, s_s = divmod(sub_secs, 60)
s_h, s_m = divmod(s_m, 60)

st.caption(f"📚 **{subject}** 누적 공부 시간: **{s_h:02d}시간 {s_m:02d}분 {s_s:02d}초**")

# 탭 구분
tab1, tab2 = st.tabs(["⏱ 스톱워치", "⏳ 타이머"])

# ----------------------------------------------------
# 4. 스톱워치 (측정 시 총 공부 시간 자동 누적)
# ----------------------------------------------------
with tab1:
    st.header(f"[{subject}] 스톱워치")
    
    # 시간 표시
    mins, secs = divmod(st.session_state.stopwatch_time, 60)
    hours, mins = divmod(mins, 60)
    
    time_display = st.empty()
    time_display.metric("현재 스톱워치 측정 시간", f"{hours:02d}:{mins:02d}:{secs:02d}")

    # 제어 버튼
    col1, col2, col3 = st.columns(3)
    
    if col1.button("▶️ 시작", key="sw_start", use_container_width=True):
        st.session_state.stopwatch_running = True
        st.rerun()
        
    if col2.button("⏸️ 정지", key="sw_stop", use_container_width=True):
        st.session_state.stopwatch_running = False
        st.rerun()
        
    if col3.button("🔄 리셋", key="sw_reset", use_container_width=True):
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_time = 0
        st.rerun()

    # 스톱워치 카운트 및 총시간 자동 증가
    if st.session_state.stopwatch_running:
        time.sleep(1)
        st.session_state.stopwatch_time += 1
        st.session_state.subject_
