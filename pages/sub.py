import time
import streamlit as st

st.set_page_config(page_title="과목별 타이머 & 스톱워치", layout="centered")

st.title("과목별 타이머 & 스톱워치")

# 과목 선택
subject = st.selectbox("과목을 선택하세요", ["국어", "수학", "영어", "탐구", "기타"])

st.divider()

# 탭 구분
tab1, tab2 = st.tabs(["⏱️ 스톱워치", "⏳ 타이머"])

# 1. 스톱워치
with tab1:
    st.header(f"[{subject}] 스톱워치")
    
    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
    if "stopwatch_time" not in st.session_state:
        st.session_state.stopwatch_time = 0

    col1, col2, col3 = st.columns(3)
    
    if col1.button("시작", key="sw_start"):
        st.session_state.stopwatch_running = True
    if col2.button("정지", key="sw_stop"):
        st.session_state.stopwatch_running = False
    if col3.button("리셋", key="sw_reset"):
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_time = 0

    time_display = st.empty()
    
    # 시간 표시 및 갱신
    mins, secs = divmod(st.session_state.stopwatch_time, 60)
    hours, mins = divmod(mins, 60)
    time_display.metric("경과 시간", f"{hours:02d}:{mins:02d}:{secs:02d}")

    if st.session_state.stopwatch_running:
        time.sleep(1)
        st.session_state.stopwatch_time += 1
        st.rerun()

# 2. 타이머
with tab2:
    st.header(f"[{subject}] 타이머")
    
    minutes_input = st.number_input("설정할 시간(분)", min_value=1, max_value=180, value=25)
    
    if st.button("타이머 시작", key="timer_start"):
        seconds = minutes_input * 60
        timer_display = st.empty()
        
        while seconds > 0:
            m, s = divmod(seconds, 60)
            timer_display.metric("남은 시간", f"{m:02d}:{s:02d}")
            time.sleep(1)
            seconds -= 1
            
        timer_display.metric("남은 시간", "00:00")
        st.success(f"[{subject}] 설정한 시간이 종료되었습니다!")
