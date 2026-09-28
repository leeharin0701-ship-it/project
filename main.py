from datetime import date
import streamlit as st

st.title("To-Do & D-Day 앱")

# 1. D-Day 계산기
st.header("D-Day 계산기")
dday_title = st.text_input("목표 이름")
target_date = st.date_input("목표 날짜", value=date.today())

if st.button("D-Day 추가"):
    if dday_title:
        today = date.today()
        diff = (target_date - today).days

        if diff == 0:
            result = "D-Day"
        elif diff > 0:
            result = f"D-{diff}"
        else:
            result = f"D+{abs(diff)}"

        st.success(f"{dday_title}: {result}")

st.divider()

# 2. To-Do 리스트
st.header("To-Do 리스트")

if "todos" not in st.session_state:
    st.session_state.todos = []

new_todo = st.text_input("할 일 입력")
if st.button("To-Do 추가"):
    if new_todo:
        st.session_state.todos.append(new_todo)
        st.rerun()

# 할 일 목록 출력
for i, todo in enumerate(st.session_state.todos):
    col1, col2 = st.columns([4, 1])
    col1.write(f"- {todo}")
    if col2.button("삭제", key=f"del_{i}"):
        st.session_state.todos.pop(i)
        st.rerun()
