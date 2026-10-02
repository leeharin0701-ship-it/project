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
# 1. 공통 데이터 세션 상태 초기화
# ----------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

# ----------------------------------------------------
# 2. 사이드바: 시간별 상세 일정 추가 양식
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

    event_color = st.color_picker("일정 색상", "#3788d8")

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
# 3. FullCalendar 옵션 설정 (제목 중복 방지 및 한국어 설정)
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
    # 중복 출력 현상을 방지하기 위한 포맷 고정
    "titleFormat": {"year": "numeric", "month": "long"},
    "slotMinTime": "06:00:00",  # 주간/일간 뷰에서 시작 시간
    "slotMaxTime": "24:00:00",  # 주간/일간 뷰에서 종료 시간
}

# 📌 캘린더 렌더링
calendar_state = calendar(
    events=st.session_state.events,
    options=calendar_options,
    key="my_calendar"
)

# ----------------------------------------------------
# 4. 전체 일정 리스트 및 삭제 기능
# ----------------------------------------------------
st.subheader("📋 전체 일정 목록")

if st.session_state.events:
    for idx, ev in enumerate(st.session_state.events):
        col_info, col_btn = st.columns([4, 1])
        
        # 시작/종료 시간 가독성 표기
        s_time_str = ev['start'].replace('T', ' ')
        e_time_str = ev['end'].replace('T', ' ')
        
        col_info.write(f"**[{s_time_str} ~ {e_time_str}]** {ev['title']}")
        
        if col_btn.button("삭제", key=f"del_ev_{idx}"):
            st.session_state.events.pop(idx)
            st.rerun()
else:
    st.info("등록된 일정이 없습니다.")
    
