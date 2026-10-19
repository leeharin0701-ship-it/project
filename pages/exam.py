import streamlit as st
import time

# 페이지 설정
st.set_page_config(
    page_title="평가원 기출문제 모의고사",
    page_icon="📝",
    layout="wide"
)

st.title("📝 과목별 평가원 기출문제 모의고사")
st.caption("한국교육과정평가원(KICE) 6월·9월 모의평가 및 수능 기출문제를 풀고 바로 채점할 수 있습니다.")

# ----------------------------------------------------
# 1. 평가원 기출 문제 데이터베이스 (예시 모의고사 데이터)
# ----------------------------------------------------
EXAM_DB = {
    "국어": [
        {
            "id": "K1",
            "year": "2024학년도 수능",
            "unit": "문학 (고전시가)",
            "question": "다음 중 고전시가에 자주 등장하는 '백일(白日)'의 관습적 상징 의미로 가장 적절한 것은?",
            "options": ["1) 임금의 은혜와 위엄", "2) 화자의 고독과 체념", "3) 속세와의 단절", "4) 세월의 무상함", "5) 자연과의 물아일체"],
            "answer": 1,
            "explanation": "고전시가에서 해(日), 백일(白日), 태양은 임금의 은혜나 군주의 임재를 상징하는 대표적 관습적 시어입니다."
        },
        {
            "id": "K2",
            "year": "2024학년도 6월 모의평가",
            "unit": "언어(문법)",
            "question": "다음 중 음운 변동 현상 중 '교체'에 해당하지 않는 것은?",
            "options": ["1) 비음화 (국물 → [궁물])", "2) 유음화 (신라 → [실라])", "3) 구개음화 (같이 → [가치])", "4) 자음군 단순화 (닭 → [닥])", "5) 된소리되기 (국밥 → [국빱])"],
            "answer": 4,
            "explanation": "자음군 단순화는 겹받침 중 하나가 사라지는 현상이므로 '탈락'에 해당합니다."
        }
    ],
    "수학": [
        {
            "id": "M1",
            "year": "2024학년도 수능",
            "unit": "대수 (지수와 로그)",
            "question": "$\\log_2 8 + \\log_3 9$ 의 값을 구하시오.",
            "options": ["1) 3", "2) 4", "3) 5", "4) 6", "5) 7"],
            "answer": 3,
            "explanation": "$\\log_2 8 = 3$, $\\log_3 9 = 2$ 이므로 $3 + 2 = 5$ 입니다."
        },
        {
            "id": "M2",
            "year": "2024학년도 9월 모의평가",
            "unit": "미적분Ⅰ (도함수)",
            "question": "함수 $f(x) = x^3 - 3x + 5$의 극댓값을 구하시오.",
            "options": ["1) 3", "2) 5", "3) 7", "4) 9", "5) 11"],
            "answer": 3,
            "explanation": "$f'(x) = 3x^2 - 3 = 3(x-1)(x+1) = 0$ 에서 $x = -1$일 때 극대입니다. $f(-1) = -1 + 3 + 5 = 7$ 입니다."
        }
    ],
    "영어": [
        {
            "id": "E1",
            "year": "2024학년도 수능",
            "unit": "어법 추론",
            "question": "다음 밑줄 친 부분 중 어법상 어색한 것을 고르시오.\n\nNot only ______ the exam, but he also achieved the highest score.",
            "options": ["1) he passed", "2) did he pass", "3) he had passed", "4) does he pass", "5) he was passing"],
            "answer": 2,
            "explanation": "문두에 부정어(Not only)가 위치하므로 주어와 조동사가 도치된 'did he pass'가 올바른 형태입니다."
        }
    ],
    "한국사": [
        {
            "id": "H1",
            "year": "2024학년도 수능",
            "unit": "조선 시대",
            "question": "다음 중 조선 영조 때 실시된 정책으로 옳은 것은?",
            "options": ["1) 노비안검법", "2) 과전법", "3) 균역법", "4) 직전법", "5) 대동법"],
            "answer": 3,
            "explanation": "영조는 군포 부담을 줄여주기 위해 군포 2필을 1필로 줄여주는 '균역법'을 실시하였습니다."
        }
    ]
}

# ----------------------------------------------------
# 2. 사이드바: 과목 및 문제 필터링
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    
    selected_subject = st.selectbox("과목 선택", list(EXAM_DB.keys()))
    questions = EXAM_DB[selected_subject]
    
    st.divider()
    st.markdown("⏱️ **시험 모드 설정**")
    time_limit_min = st.number_input("제한 시간(분)", min_value=1, max_value=60, value=10)
    
    if st.button("🔄 처음부터 다시 풀기", use_container_width=True):
        st.session_state[f"answers_{selected_subject}"] = {}
        st.session_state[f"submitted_{selected_subject}"] = False
        st.rerun()

# 세션 상태 초기화
if f"answers_{selected_subject}" not in st.session_state:
    st.session_state[f"answers_{selected_subject}"] = {}

if f"submitted_{selected_subject}" not in st.session_state:
    st.session_state[f"submitted_{selected_subject}"] = False

# ----------------------------------------------------
# 3. 메인 문제 풀이 UI
# ----------------------------------------------------
st.subheader(f"📌 [{selected_subject}] 평가원 기출 문제 ({len(questions)}문항)")

# 제출 완료 여부 확인
is_submitted = st.session_state[f"submitted_{selected_subject}"]

# OMR 응답 저장용
user_answers = st.session_state[f"answers_{selected_subject}"]

for idx, q in enumerate(questions, 1):
    st.markdown(f"#### **Q{idx}. [{q['year']}] {q['unit']}**")
    st.markdown(f"**{q['question']}**")
    
    # 정답 제출 전: 라디오 버튼 선택 가능
    if not is_submitted:
        selected_option = st.radio(
            f"답안 선택 (Q{idx})",
            options=q["options"],
            key=f"radio_{q['id']}",
            index=None,
            label_visibility="collapsed"
        )
        if selected_option:
            # 선택한 번호 저장 (문자열 앞의 숫자만 추출)
            ans_num = int(selected_option[0])
            user_answers[q['id']] = ans_num
    
    # 정답 제출 후: 채점 결과 및 해설 표시
    else:
        user_ans = user_answers.get(q['id'], None)
        correct_ans = q['answer']
        
        if user_ans == correct_ans:
            st.success(f"⭕ **정답입니다!** (선택한 답: {user_ans}번)")
        elif user_ans is None:
            st.warning(f"⚠️ **미응답** (정답: {correct_ans}번)")
        else:
            st.error(f"❌ **오답입니다.** (선택한 답: {user_ans}번 / 정답: {correct_ans}번)")
            
        with st.expander("💡 문제 해설 보기", expanded=True):
            st.write(q['explanation'])
            
    st.divider()

# ----------------------------------------------------
# 4. 제출 및 채점 결과
# ----------------------------------------------------
if not is_submitted:
    if st.button("📥 OMR 최종 제출 및 채점하기", type="primary", use_container_width=True):
        st.session_state[f"submitted_{selected_subject}"] = True
        st.rerun()
else:
    # 점수 계산
    correct_count = 0
    for q in questions:
        if user_answers.get(q['id']) == q['answer']:
            correct_count += 1
            
    total_count = len(questions)
    score = int((correct_count / total_count) * 100)
    
    st.subheader("📊 채점 결과")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 문항 수", f"{total_count}문제")
    col2.metric("맞힌 문항 수", f"{correct_count}문제")
    col3.metric("최종 점수", f"{score}점")
    
    if score == 100:
        st.balloons()
        st.success("🎉 만점입니다! 완벽하게 이해하셨네요.")
    elif score >= 60:
        st.info("👍 잘하셨습니다! 오답 해설을 확인하고 복습해보세요.")
    else:
        st.warning("💪 틀린 문제를 오답노트로 복습해보세요.")
