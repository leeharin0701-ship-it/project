from datetime import date
import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="To-Do & D-Day", layout="centered")

# 명언 데이터
quotes = [
    ("삶이 있는 한 희망은 있다.", "키케로"),
    ("산다는것 그것은 격렬한 유희이다.", "아인슈타인"),
    ("하루에 3시간을 걸으면 7년 후에 지구를 한 바퀴 돌 수 있다.", "사무엘 존슨"),
    ("언제나 현재에 집중할수 있다면 행복할것이다.", "파울로 코엘료"),
    ("진정으로 웃으려면 자신의 고통을 가지고 놀 줄 알아야 한다.", "찰리 채플린"),
]

# 재접속 시마다 랜덤 선택
if "today_quote" not in st.session_state:
    st.session_state.today_quote = random.choice(quotes)

quote_text, quote_author = st.session_state.today_quote

# 오른쪽 상단 명언 표시
col_title, col_quote = st.columns([1, 1])
with col_quote:
    st.markdown(
        f"<div style='text-align: right; color: gray; font-size: 0.85em;'>"
        f"<i>\"{quote_text}\"</i><br><b>- {quote_author} -</b>"
        f"</div>",
        unsafe_allow_html=True
    )

st.title("To-Do & D-Day 앱")

# 1. D-Day 계산기
st.header("D-Day 계산기")

dday_title = st.text_input("목표 이름", key="dday_title_input")
target_date = st.date_input("목표 날짜", value=date.today())

if st.button("D-Day 계산"):
    if dday_title:
        today = date.today()
        diff = (target_date - today).days

        if diff == 0:
            result = "D-Day"
        elif diff > 0:
            result = f"D-{diff}"
        else:
            result = f"D+{abs(diff)}"

        st.info(f"**{dday_title}**: {result}")
    else:
        st.warning("목표 이름을 입력하세요.")

st.divider()

# 2. To-Do 리스트
st.header("To-Do 리스트")

# 세션 상태 초기화
if "todos" not in st.session_state:
    st.session_state.todos = []

# 할 일 입력
new_todo = st.text_input("할 일 입력", key="todo_input")

if st.button("할 일 추가"):
    if new_todo:
        st.session_state.todos.append(new_todo)
        st.rerun()

# 할 일 목록 및 삭제 기능
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([4, 1])
        col1.write(f"- {todo}")
        if col2.button("삭제", key=f"del_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()
else:
    st.caption("등록된 할 일이 없습니다.")
