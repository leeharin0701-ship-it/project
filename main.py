from datetime import date
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="To-Do & D-Day", layout="centered")

# 외부 API에서 무작위 명언 가져오는 함수
def get_random_quote():
    try:
        response = requests.get("https://api.quotable.io/random", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data["content"], data["author"]
    except Exception:
        pass
    return "삶이 있는 한 희망은 있다.", "키케로"

# 명언 및 D-Day 세션 상태 초기화
if "today_quote" not in st.session_state:
    st.session_state.today_quote = get_random_quote()

if "dday_data" not in st.session_state:
    st.session_state.dday_data = None

quote_text, quote_author = st.session_state.today_quote

# 상단 레이아웃: 왼쪽(상단 중앙 D-Day/제목), 오른쪽(명언)
col_main, col_quote = st.columns([2, 1])

with col_quote:
    st.markdown(
        f"<div style='text-align: right; color: gray; font-size: 0.85em;'>"
        f"<i>\"{quote_text}\"</i><br><b>- {quote_author} -</b>"
        f"</div>",
        unsafe_allow_html=True
    )

with col_main:
    st.title("To-Do & D-Day 앱")

# 1. D-Day 표시 및 설정 영역
if st.session_state.dday_data is None:
    st.subheader("D-Day 설정")
    dday_title = st.text_input("목표 이름", key="dday_title_input")
    target_date = st.date_input("목표 날짜", value=date.today())

    if st.button("D-Day 설정"):
        if dday_title:
            st.session_state.dday_data = {
                "title": dday_title,
                "target_date": target_date
            }
            st.rerun()
        else:
            st.warning("목표 이름을 입력하세요.")
else:
    # D-Day 계산
    title = st.session_state.dday_data["title"]
    target_date = st.session_state.dday_data["target_date"]
    today = date.today()
    diff = (target_date - today).days

    if diff == 0:
        dday_str = "D-DAY"
    elif diff > 0:
        dday_str = f"D-{diff:02d}"
    else:
        dday_str = f"D+{abs(diff):02d}"

    # 화면 중앙 상단에 큰 글씨로 D-Day 표시
    st.markdown(
        f"""
        <div style='text-align: center; margin: 10px 0 20px 0;'>
            <span style='font-size: 1.2em; color: #555;'>{title}</span><br>
            <span style='font-size: 3em; font-weight: bold; color: #E74C3C;'>{dday_str}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("D-Day 재설정", key="reset_dday"):
        st.session_state.dday_data = None
        st.rerun()

st.divider()

# 2. To-Do 리스트
st.header("To-Do 리스트")

if "todos" not in st.session_state:
    st.session_state.todos = []

new_todo = st.text_input("할 일 입력", key="todo_input")

if st.button("할 일 추가"):
    if new_todo:
        st.session_state.todos.append({"text": new_todo, "done": False})
        st.rerun()

if st.session_state.todos:
    for i, item in enumerate(st.session_state.todos):
        col1, col2 = st.columns([4, 1])
        
        if item["done"]:
            col1.markdown(f"~{item['text']}~")
        else:
            col1.write(f"- {item['text']}")
            
        btn_label = "취소" if item["done"] else "완료"
        if col2.button(btn_label, key=f"toggle_{i}"):
            st.session_state.todos[i]["done"] = not st.session_state.todos[i]["done"]
            st.rerun()
else:
    st.caption("등록된 할 일이 없습니다.")
