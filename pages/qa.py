import requests
import streamlit as st

st.set_page_config(page_title="과목별 AI 질문하기", layout="centered")

st.title("🤖 과목별 AI 질문하기")

# 사이드바에 Hugging Face 토큰 입력
hf_token = st.sidebar.text_input("Hugging Face Token 입력 (hf_...)", type="password")

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

# Hugging Face Inference API 호출 함수
def query_huggingface(prompt_text, token):
    # 무료 모델 사용 (Qwen/Qwen2.5-7B-Instruct)
    api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "inputs": f"<|im_start|>system\n당신은 친절한 {subject} 선생님입니다. 학생의 질문에 이해하기 쉽게 한국어로 답변하세요.<|im_end|>\n<|im_start|>user\n{prompt_text}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    response = requests.post(api_url, headers=headers, json=payload, timeout=20)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "답변을 생성하지 못했습니다.")
    elif response.status_code == 503:
        return "모델을 로딩 중입니다. 10~20초 후 다시 시도해 주세요!"
    
    return f"오류가 발생했습니다. (코드: {response.status_code})"

# 질문 입력 및 처리
if prompt := st.chat_input(f"[{subject}] 관련 질문을 입력하세요..."):
    if not hf_token:
        st.error("사이드바에 Hugging Face 토큰을 입력해 주세요.")
    else:
        # 사용자 질문 표시 및 저장
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # AI 답변 생성
        with st.chat_message("assistant"):
            with st.spinner("AI 선생님이 답변을 작성 중입니다..."):
                ai_reply = query_huggingface(prompt, hf_token)
                st.markdown(ai_reply)

        # AI 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
