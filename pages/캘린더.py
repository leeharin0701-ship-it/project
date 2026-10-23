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

if "selected_date_str" not in st.session_state:
    st.session_state.selected_date_str = str(date.today())

if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

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
# 3. 팝업 창 (날짜 클릭 시 뜨는 입력 모달)
# ----------------------------------------------------
@st.dialog("📌 새 일정 추가하기")
def add_event_popup(default_date_str):
    st.write(f"선택한 날짜: **{default_date_str}**")
    
    with st.form("popup_event_form"):
        popup_title = st.text_input("일정 제목", placeholder="할 일을 입력하세요")
        is_all_day = st.checkbox("하루 종일 (시간 미지정)", value=True)
        
        d_val = datetime.strptime(default_date_str, "%Y-%m-%d").date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_d = st.date_input("시작 날짜", value=d_val)
        with col2:
            end_d = st.date_input("종료 날짜", value=d_val)
            
        selected_color_name = st.selectbox("일정 색상", options=list(COLOR_PALETTE.keys()))
        event_color = COLOR_PALETTE[selected_color_name]
        
        submitted = st.form_submit_button("일정 등록", use_container_width=True)
        if submitted:
            if popup_title.strip():
                new_event = {
                    "title": popup_title.strip(),
                    "start": start_d.isoformat(),
                    "end": end_d.isoformat(),
                    "allDay": is_all_day,
                    "color": event_color
                }
                st.session_state.events.append(new_event)
                st.success("일정이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("일정 제목을 입력해주세요.")

# ----------------------------------------------------
# 4. 사이드바: 기본 일정 추가 메뉴
# ----------------------------------------------------
with st.sidebar:
    st.header("➕ 새 일정 추가")
    st.caption("💡 캘린더의 날짜를 클릭하면 팝업창이 뜹니다!")
    
    if st.button("➕ 날짜 선택하여 일정 추가", use_container_width=True):
        st.session_state.show_popup = True

    st.divider()
    if st.button("🧹 모든 일정 초기화", use_container_width=True):
        st.session_state.events = []
        st.rerun()

# 사이드바 버튼이나 팝업 상태 체크
if st.session_state.show_popup:
    st.session_state.show_popup = False
    add_event_popup(st.session_state.selected_date_str)

# ----------------------------------------------------
# 5. FullCalendar 설정 및 클릭 이벤트 처리
# ----------------------------------------------------
calendar_options = {
    "editable": True,
    "selectable": True,
    "selectMirror": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay,listMonth",
    },
    "initialView": "dayGridMonth",
    "locale": "ko",
    "titleFormat": {"year": "numeric", "month": "long"},
}

calendar_data = calendar(
    events=st.session_state.events,
    options=calendar_options,
    key="my_calendar"
)

# 📌 날짜 클릭 시 엉뚱한 값으로 뜨던 버그 수정 (dateStr 활용)
if calendar_data:
    if calendar_data.get("dateClick"):
        # dateStr을 사용하면 시간대 밀림 현상 없이 정확한 YYYY-MM-DD를 가져옵니다.
        clicked_date = calendar_data["dateClick"].get("dateStr")
        if clicked_date:
            st.session_state.selected_date_str = clicked_date[:10]
            add_event_popup(st.session_state.selected_date_str)
            
    elif calendar_data.get("select"):
        start_str = calendar_data["select"].get("start")
        if start_str:
            st.session_state.selected_date_str = start_str[:10]
            add_event_popup(st.session_state.selected_date_str)

# ----------------------------------------------------
# 6. 전체 일정 목록 및 삭제
# ----------------------------------------------------
st.divider()
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
