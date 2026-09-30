import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="과목별 AI 질문하기", layout="centered")

st.title("🤖 과목별 AI 질문하기")

# OpenAI API 키 입력 (사이드바)
api_key = st.sidebar.text_input("OpenAI API Key 입력", type="password")

# 과목 선택
subject = st.selectbox(
    "질문할 과목을 선택하세요",
    ["국어", "수학", "영어", "한국사", "사회", "과학", "기타"]
)

# 대화 기록 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 질문 입력 처리
if prompt := st.chat_input(f"[{subject}] 관련 질문을 입력하세요..."):
    if not api_key:
        st.error("API 키를 사이드바에 먼저 입력해 주세요.")
    else:
        client = OpenAI(api_key=api_key)

        # 사용자 메시지 표시 및 저장
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI 답변 생성
        with st.chat_message("assistant"):
            # 과목 맞춤형 역할 지정
            system_prompt = f"당신은 친절한 {subject} 선생님입니다. 학생의 질문에 핵심만 쉽고 알기 않게 설명하세요."
            
            messages_to_send = [{"role": "system", "content": system_prompt}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_to_send
            )
            
            ai_reply = response.choices[0].message.content
            st.markdown(ai_reply)

        # AI 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
