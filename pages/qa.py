import requests
import streamlit as st

st.set_page_config(page_title="과목별 AI 질문하기", layout="centered")

st.title("🤖 과목별 AI 질문하기")

# Streamlit Secrets에서 토큰 자동 불러오기
try:
    hf_token = st.secrets["HF_TOKEN"]
except Exception:
    hf_token = None

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

# Hugging Face Router API 호출 함수
def query_huggingface(prompt_text, token):
    api_url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 안정적으로 제공되는 Llama-3.2-3B-Instruct 모델로 변경
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": f"당신은 친절한 {subject} 선생님입니다. 학생의 질문에 쉽고 명확하게 한국어로 답변하세요."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "❌ **토큰 오류**: Secrets에 설정된 Hugging Face 토큰이 올바르지 않습니다."
        elif response.status_code == 503:
            return "⏳ **모델 로딩 중**: AI 서버가 준비 중입니다. 10초 뒤에 다시 질문해 주세요!"
        else:
            return f"❌ **오류 발생**: (응답 코드: {response.status_code}) - {response.text}"
            
    except requests.exceptions.Timeout:
        return "⚠️ 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요."
    except Exception as e:
        return f"⚠️ 에러 발생: {str(e)}"

# 질문 입력 및 처리
if prompt := st.chat_input(f"[{subject}] 관련 질문을 입력하세요..."):
    if not hf_token:
        st.error("Streamlit Secrets에 'HF_TOKEN'이 설정되지 않았습니다. `.streamlit/secrets.toml` 설정을 확인해 주세요.")
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
