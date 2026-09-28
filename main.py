from datetime import date
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="To-Do & D-Day", layout="centered")

# 외부 API에서 무작위 명언 가져오는 함수
def get_random_quote():
    try:
        # API 호출 (타임아웃 3초 설정)
        response = requests.get("https://api.quotable.io/random", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data["content"], data["author"]
    except Exception:
        pass
    # 네트워크 오류 등 API 호출 실패 시 기본 명언 반환
    return "삶이 있는 한 희망은 있다.", "키케로"

# 새로고침/재접속 시마다 새로운 명언 불러오기
quote_text, quote_author = get_random_quote()

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
