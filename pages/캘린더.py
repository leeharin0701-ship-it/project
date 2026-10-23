from datetime import datetime, date, time
import streamlit as st
from streamlit_calendar import calendar

# 페이지 기본 설정
st.set_page_config(
    page_title="일정 캘린더",
    page_icon="📅",
    layout="wide"
)

st.title("📅 일정 캘린더")

# ----------------------------------------------------
# 1. 세션 상태 초기화
# ----------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

# ----------------------------------------------------
# 2. 대표 8가지 일정 색상 팔레트 정의
# ----------------------------------------------------
COLOR_PALETTE = {
    "🔵 블루": "#3788d8",
    "🟢 그린": "#27ae60",
    "🔴 레드": "#e74c3c",
    "🟡 옐로우": "#f39c12",
    "🟣 퍼플": "#8e44ad",
    "🟠 오렌지": "#e67e22",
    "🪨 그레이": "#7f8c8d",
    "🩷 핑크": "#fd79a8"
}

# ----------------------------------------------------
# 3. 사이드바: 시간/날짜별 상세 일정 추가
# ----------------------------------------------------
with st.sidebar:
    st.header("➕ 새 일정 추가")
    
    event_title = st.text_input("일정 제목")
    is_all_day = st.checkbox("하루 종일 (시간 미지정)", value=False)
    
    col_s_date, col_s_time = st.columns(2)
    with col_s_date:
        start_d = st.date_input("시작 날짜", value=date.today())
    with col_s_time:
        start_t = st.time_input("시작 시간", value=time(9, 0)) if not is_all_day else None

    col_e_date, col_e_time = st.columns(2)
    with col_e_date:
        end_d = st.date_input("종료 날짜", value=date.today())
    with col_e_time:
        end_t = st.time_input("종료 시간", value=time(10, 0)) if not is_all_day else None

    # 8가지 단일 컬러 선택 라디오 버튼
    st.markdown("**일정 색상 선택**")
    selected_color_name = st.radio(
        "일정 색상 선택",
        options=list(COLOR_PALETTE.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )
    event_color = COLOR_PALETTE[selected_color_name]

    if st.button("캘린더에 일정 추가", use_container_width=True):
        if event_title:
            if is_all_day:
                start_str = start_d.isoformat()
                end_str = end_d.isoformat()
            else:
                start_dt = datetime.combine(start_d, start_t)
                end_dt = datetime.combine(end_d, end_t)
                
                if start_dt > end_dt:
                    st.error("시작 시간이 종료 시간보다 늦을 수 없습니다.")
                    st.stop()
                    
                start_str = start_dt.isoformat()
                end_str = end_dt.isoformat()

            new_event = {
                "title": event_title,
                "start": start_str,
                "end": end_str,
                "allDay": is_all_day,
                "color": event_color
            }
            st.session_state.events.append(new_event)
            st.success("일정이 추가되었습니다!")
            st.rerun()
        else:
            st.warning("일정 제목을 입력하세요.")

    st.divider()
    if st.button("🧹 모든 일정 초기화", use_container_width=True):
        st.session_state.events = []
        st.rerun()

# ----------------------------------------------------
# 4. FullCalendar 설정
# ----------------------------------------------------
calendar_options = {
    "editable": True,
    "selectable": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay,listMonth",
    },
    "initialView": "dayGridMonth",
    "locale": "ko",
    "titleFormat": {"year": "numeric", "month": "long"},
    "slotMinTime": "06:00:00",
    "slotMaxTime": "24:00:00",
}

# 📌 캘린더 출력
calendar(
    events=st.session_state.events,
    options=calendar_options,
    key="my_calendar"
)

# ----------------------------------------------------
# 5. 전체 일정 목록 및 개별 삭제
# ----------------------------------------------------
st.subheader("📋 전체 일정 목록")

if st.session_state.events:
    for idx, ev in enumerate(st.session_state.events):
        col_info, col_btn = st.columns([4, 1])
        
        s_time_str = ev['start'].replace('T', ' ')
        e_time_str = ev['end'].replace('T', ' ')
        
        col_info.write(f"**[{s_time_str} ~ {e_time_str}]** {ev['title']}")
        
        if col_btn.button("삭제", key=f"del_ev_{idx}"):
            st.session_state.events.pop(idx)
            st.rerun()
else:
    st.info("등록된 일정이 없습니다.")
