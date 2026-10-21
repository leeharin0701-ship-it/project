import time
import streamlit as st

st.set_page_config(page_title="과목별 타이머 & 스톱워치", page_icon="⏱️", layout="centered")

# ----------------------------------------------------
# 1. 세션 상태 안전 초기화 (KeyError 방지)
# ----------------------------------------------------
# 과목 목록 정의
SUBJECT_LIST = ["국어", "수학", "영어", "탐구", "기타"]

# 딕셔너리가 없으면 새로 생성
if "subject_study_time" not in st.session_state:
    st.session_state.subject_study_time = {sub: 0 for sub in SUBJECT_LIST}

# 기존 세션에 누락된 과목 키가 있다면 자동 보완 (KeyError 방지)
for sub in SUBJECT_LIST:
    if sub not in st.session_state.subject_study_time:
        st.session_state.subject_study_time[sub] = 0

if "stopwatch_running" not in st.session_state:
    st.session_state.stopwatch_running = False
if "stopwatch_time" not in st.session_state:
    st.session_state.stopwatch_time = 0

if "timer_active" not in st.session_state:
    st.session_state.timer_active = False
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# ----------------------------------------------------
# 2. 상단 레이아웃 (총 공부 시간 계산)
# ----------------------------------------------------
col_title, col_total = st.columns([1.5, 1])

# KeyError 없이 안전하게 총시간 합산
total_seconds = sum(st.session_state.subject_study_time.values())
t_mins, t_secs = divmod(total_seconds, 60)
t_hours, t_mins = divmod(t_mins, 60)

with col_title:
    st.title("⏱️ 과목별 타이머")

with col_total:
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
# 3. 과목 선택
# ----------------------------------------------------
subject = st.selectbox("과목을 선택하세요", SUBJECT_LIST)

# 안전하게 선택된 과목의 공부 시간 가져오기 (없으면 0)
sub_secs = st.session_state.subject_study_time.get(subject, 0)
s_m, s_s = divmod(sub_secs, 60)
s_h, s_m = divmod(s_m, 60)

st.caption(f"📚 **{subject}** 누적 공부 시간: **{s_h:02d}시간 {s_m:02d}분 {s_s:02d}초**")

tab1, tab2 = st.tabs(["⏱ 스톱워치", "⏳ 타이머"])

# ----------------------------------------------------
# 4. 스톱워치
# ----------------------------------------------------
with tab1:
    st.header(f"[{subject}] 스톱워치")
    
    mins, secs = divmod(st.session_state.stopwatch_time, 60)
    hours, mins = divmod(mins, 60)
    
    time_display = st.empty()
    time_display.metric("현재 스톱워치 측정 시간", f"{hours:02d}:{mins:02d}:{secs:02d}")

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

    if st.session_state.stopwatch_running:
        time.sleep(1)
        st.session_state.stopwatch_time += 1
        
        # 키가 존재하는지 안전하게 확인 후 1초 증가
        if subject not in st.session_state.subject_study_time:
            st.session_state.subject_study_time[subject] = 0
        st.session_state.subject_study_time[subject] += 1
        
        st.rerun()

# ----------------------------------------------------
# 5. 타이머
# ----------------------------------------------------
with tab2:
    st.header(f"[{subject}] 타이머")

    if not st.session_state.timer_active:
        minutes_input = st.number_input("설정할 시간(분)", min_value=1, max_value=180, value=25)
        
        if st.button("🚀 타이머 시작", key="timer_start_init", use_container_width=True):
            st.session_state.timer_seconds = minutes_input * 60
            st.session_state.timer_active = True
            st.session_state.timer_running = True
            st.rerun()
    else:
        m, s = divmod(st.session_state.timer_seconds, 60)
        timer_display = st.empty()
        timer_display.metric("남은 시간", f"{m:02d}:{s:02d}")

        t_col1, t_col2 = st.columns(2)
        
        if st.session_state.timer_running:
            if t_col1.button("⏸️ 일시정지", key="timer_pause", use_container_width=True):
                st.session_state.timer_running = False
                st.rerun()
        else:
            if t_col1.button("▶️ 재개", key="timer_resume", use_container_width=True):
                st.session_state.timer_running = True
                st.rerun()

        if t_col2.button("❌ 취소 및 설정으로", key="timer_cancel", use_container_width=True):
            st.session_state.timer_active = False
            st.session_state.timer_running = False
            st.session_state.timer_seconds = 0
            st.rerun()

        if st.session_state.timer_running and st.session_state.timer_seconds > 0:
            time.sleep(1)
            st.session_state.timer_seconds -= 1
            
            # 키가 존재하는지 안전하게 확인 후 1초 증가
            if subject not in st.session_state.subject_study_time:
                st.session_state.subject_study_time[subject] = 0
            st.session_state.subject_study_time[subject] += 1
            
            st.rerun()
        elif st.session_state.timer_running and st.session_state.timer_seconds == 0:
            st.session_state.timer_running = False
            st.balloons()
            st.success(f"🎉 [{subject}] 설정한 시간이 종료되었습니다!")
