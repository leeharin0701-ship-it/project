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
# 1. 세션 상태 초기화
# ----------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

if "selected_date" not in st.session_state:
    st.session_state.selected_date = str(date.today())

if "open_dialog" not in st.session_state:
    st.session_state.open_dialog = False

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
# 3. 캘린더 클릭 시 뜨는 모달 팝업 정의
# ----------------------------------------------------
@st.dialog("📌 새 일정 추가하기")
def add_event_dialog(date_str):
    st.write(f"선택한 날짜: **{date_str}**")
    
    with st.form("modal_event_form"):
        popup_title = st.text_input("일정 제목", placeholder="할 일을 입력하세요")
        is_all_day = st.checkbox("하루 종일 (시간 미지정)", value=True)
        
        d_val = datetime.strptime(date_str, "%Y-%m-%d").date()
        
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
                st.session_state.open_dialog = False  # 팝업 닫기
                st.success("일정이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("일정 제목을 입력해주세요.")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 캘린더 관리")
    if st.button("🧹 모든 일정 초기화", use_container_width=True):
        st.session_state.events = []
        st.rerun()

# ----------------------------------------------------
# 4. FullCalendar 설정 및 클릭 감지
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

# 📌 캘린더 날짜 칸을 클릭했을 때 상태를 True로 변경하고 즉시 리런
if calendar_data:
    if calendar_data.get("dateClick"):
        clicked_date = calendar_data["dateClick"].get("dateStr")
        if clicked_date:
            st.session_state.selected_date = clicked_date[:10]
            st.session_state.open_dialog = True
            st.rerun()
            
    elif calendar_data.get("select"):
        start_str = calendar_data["select"].get("start")
        if start_str:
            st.session_state.selected_date = start_str[:10]
            st.session_state.open_dialog = True
            st.rerun()

# 📌 팝업 상태가 활성화되어 있으면 다이얼로그 띄우기
if st.session_state.open_dialog:
    add_event_dialog(st.session_state.selected_date)

# ----------------------------------------------------
# 5. 전체 일정 목록 및 삭제
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
