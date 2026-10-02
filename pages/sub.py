import time
import streamlit as st

st.set_page_config(page_title="과목별 타이머 & 스톱워치", layout="centered")

st.title("과목별 타이머 & 스톱워치")

# 과목 선택
subject = st.selectbox("과목을 선택하세요", ["국어", "수학", "영어", "탐구", "기타"])

st.divider()

# 탭 구분
tab1, tab2 = st.tabs(["⏱️️ 스톱워치", "⏳ 타이머"])

# ----------------------------------------------------
# 1. 스톱워치
# ----------------------------------------------------
with tab1:
    st.header(f"[{subject}] 스톱워치")
    
    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
    if "stopwatch_time" not in st.session_state:
        st.session_state.stopwatch_time = 0

    # ① 시간 표시를 상단에 배치
    mins, secs = divmod(st.session_state.stopwatch_time, 60)
    hours, mins = divmod(mins, 60)
    
    time_display = st.empty()
    time_display.metric("경과 시간", f"{hours:02d}:{mins:02d}:{secs:02d}")

    # ② 버튼들을 숫자(시간) 아래에 배치
    col1, col2, col3 = st.columns(3)
    
    if col1.button("시작", key="sw_start", use_container_width=True):
        st.session_state.stopwatch_running = True
    if col2.button("정지", key="sw_stop", use_container_width=True):
        st.session_state.stopwatch_running = False
    if col3.button("리셋", key="sw_reset", use_container_width=True):
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_time = 0
        st.rerun()

    # 스톱워치 1초 간격 루프
    if st.session_state.stopwatch_running:
        time.sleep(1)
        st.session_state.stopwatch_time += 1
        st.rerun()

# ----------------------------------------------------
# 2. 타이머
# ----------------------------------------------------
with tab2:
    st.header(f"[{subject}] 타이머")

    # 세션 상태 초기화
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = False  # 타이머 화면 전환 여부
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False  # 타이머 카운트다운 진행 여부
    if "timer_seconds" not in st.session_state:
        st.session_state.timer_seconds = 0

    # ① 타이머가 시작되지 않았을 때 (설정 화면)
    if not st.session_state.timer_active:
        minutes_input = st.number_input("설정할 시간(분)", min_value=1, max_value=180, value=25)
        
        if st.button("타이머 시작", key="timer_start_init", use_container_width=True):
            st.session_state.timer_seconds = minutes_input * 60
            st.session_state.timer_active = True
            st.session_state.timer_running = True
            st.rerun()

    # ② 타이머가 작동 중이거나 일시정지 상태일 때 (타이머 진행 화면)
    else:
        # 남은 시간 계산 및 표시
        m, s = divmod(st.session_state.timer_seconds, 60)
        timer_display = st.empty()
        timer_display.metric("남은 시간", f"{m:02d}:{s:02d}")

        # 제어 버튼 (일시정지 / 시작 / 취소)
        t_col1, t_col2 = st.columns(2)
        
        if st.session_state.timer_running:
            if t_col1.button("일시정지", key="timer_pause", use_container_width=True):
                st.session_state.timer_running = False
                st.rerun()
        else:
            if t_col1.button("재개", key="timer_resume", use_container_width=True):
                st.session_state.timer_running = True
                st.rerun()

        if t_col2.button("취소 및 설정으로", key="timer_cancel", use_container_width=True):
            st.session_state.timer_active = False
            st.session_state.timer_running = False
            st.session_state.timer_seconds = 0
            st.rerun()

        # 카운트다운 진행
        if st.session_state.timer_running and st.session_state.timer_seconds > 0:
            time.sleep(1)
            st.session_state.timer_seconds -= 1
            st.rerun()
        elif st.session_state.timer_running and st.session_state.timer_seconds == 0:
            st.session_state.timer_running = False
            st.success(f"🎉 [{subject}] 설정한 시간이 종료되었습니다!")
