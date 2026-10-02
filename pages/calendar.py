from datetime import datetime, date
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
# 1. 세션 상태에 이벤트 저장 공간 초기화
# ----------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = [
        {
            "title": "팀 미팅",
            "start": date.today().isoformat(),
            "end": date.today().isoformat(),
            "color": "#3788d8"
        }
    ]

# ----------------------------------------------------
# 2. 사이드바: 일정 추가 양식
# ----------------------------------------------------
with st.sidebar:
    st.header("➕ 새 일정 추가")
    event_title = st.text_input("일정 제목")
    
    col_start, col_end = st.columns(2)
    with col_start:
        start_date = st.date_input("시작일", value=date.today())
    with col_end:
        end_date = st.date_input("종료일", value=date.today())
        
    event_color = st.color_picker("일정 색상", "#3788d8")

    if st.button("캘린더에 추가", use_container_width=True):
        if event_title:
            if start_date > end_date:
                st.error("시작일은 종료일보다 이전이어야 합니다.")
            else:
                new_event = {
                    "title": event_title,
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "color": event_color
                }
                st.session_state.events.append(new_event)
                st.success("일정이 추가되었습니다!")
                st.rerun()
        else:
            st.warning("일정 제목을 입력하세요.")

    st.divider()
    
    # 일정 전체 삭제 옵션
    if st.button("🧹 모든 일정 초기화", use_container_width=True):
        st.session_state.events = []
        st.rerun()

# ----------------------------------------------------
# 3. FullCalendar 옵션 설정
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
    "locale": "ko",  # 한글 언어 설정
}

# 📌 캘린더 출력
calendar_state = calendar(
    events=st.session_state.events,
    options=calendar_options,
    key="my_calendar"
)

# ----------------------------------------------------
# 4. 등록된 일정 리스트 하단 표시 및 개별 삭제 기능
# ----------------------------------------------------
st.subheader("📋 등록된 일정 목록")

if st.session_state.events:
    for idx, ev in enumerate(st.session_state.events):
        col_info, col_btn = st.columns([4, 1])
        col_info.write(f"**[{ev['start']} ~ {ev['end']}]** {ev['title']}")
        if col_btn.button("삭제", key=f"del_ev_{idx}"):
            st.session_state.events.pop(idx)
            st.rerun()
else:
    st.info("등록된 일정이 없습니다.")
