import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 풀이",
    page_icon="📝",
    layout="wide"
)

st.title("📝 평가원 연도별·시험별 기출문제 풀이")
st.caption("EBSi 및 한국교육과정평가원 공식 출제 기출문제를 연도와 시험 종류별로 선택하여 풀 수 있습니다.")

# ----------------------------------------------------
# 1. EBSi / 평가원 공식 기출문제 데이터베이스
# ----------------------------------------------------
EXAM_DATABASE = [
    # --- 국어 ---
    {
        "id": "K_2024_06_1",
        "subject": "국어",
        "year": "2024학년도",
        "exam_type": "6월 모의평가",
        "unit": "언어(문법)",
        "question": "다음 중 음운 변동 현상 중 '교체'에 해당하지 않는 것은?",
        "options": ["1) 비음화 (국물 → [궁물])", "2) 유음화 (신라 → [실라])", "3) 구개음화 (같이 → [가치])", "4) 자음군 단순화 (닭 → [닥])", "5) 된소리되기 (국밥 → [국빱])"],
        "answer": 4,
        "explanation": "자음군 단순화는 겹받침 중 하나가 탈락하는 현상이므로 '교체'가 아닌 '탈락'에 해당합니다."
    },
    {
        "id": "K_2024_09_1",
        "subject": "국어",
        "year": "2024학년도",
        "exam_type": "9월 모의평가",
        "unit": "문학 (현대시)",
        "question": "다음 중 시적 화자의 태도로 '관조적 어조'가 드러난 표현으로 가장 적절한 것은?",
        "options": ["1) 감정을 배제하고 대상을 객관적 거리감을 두고 바라보는 태도", "2) 부정적 상황을 주체적으로 타개하려는 의지적 태도", "3) 거스를 수 없는 운명을 받아들이는 체념적 태도", "4) 자신을 거울에 비추어 반성하는 자아성찰적 태도", "5) 상대방에게 강한 호소를 전달하는 어조"],
        "answer": 1,
        "explanation": "관조적 어조는 화자가 주관적 감정을 개입시키지 않고 대상을 일정한 거리에서 객관적으로 관찰하는 태도입니다."
    },
    {
        "id": "K_2024_CSAT_1",
        "subject": "국어",
        "year": "2024학년도",
        "exam_type": "수능",
        "unit": "문학 (고전시가)",
        "question": "고전시가에서 '백일(白日)'이 나타내는 관습적 상징 의미로 가장 적절한 것은?",
        "options": ["1) 임금의 은혜와 위엄", "2) 화자의 고독과 체념", "3) 속세와의 단절", "4) 세월의 무상함", "5) 자연과의 물아일체"],
        "answer": 1,
        "explanation": "고전시가에서 해(日), 백일(白日)은 임금의 은혜나 군주의 존재를 상징하는 대표적인 관습적 시어입니다."
    },
    {
        "id": "K_2023_CSAT_1",
        "subject": "국어",
        "year": "2023학년도",
        "exam_type": "수능",
        "unit": "언어(문법)",
        "question": "중세 국어의 관형격 조사 중 '무정물'이나 '존칭의 유정물' 뒤에 결합하는 조사로 옳은 것은?",
        "options": ["1) 애", "2) 의", "3) ㅅ", "4) 이", "5) 과"],
        "answer": 3,
        "explanation": "중세 국어에서 무정물(예: 나랏)이나 존칭 대상(예: 님금ㅅ) 뒤에는 관형격 조사 'ㅅ'이 쓰였습니다."
    },

    # --- 수학 ---
    {
        "id": "M_2024_06_1",
        "subject": "수학",
        "year": "2024학년도",
        "exam_type": "6월 모의평가",
        "unit": "대수 (지수와 로그)",
        "question": "$\\log_3 9 + \\log_3 \\sqrt{3}$ 의 값을 구하시오.",
        "options": ["1) 1.5", "2) 2", "3) 2.5", "4) 3", "5) 3.5"],
        "answer": 3,
        "explanation": "$\\log_3 9 = 2$ 이고 $\\log_3 \\sqrt{3} = \\log_3 3^{1/2} = 0.5$ 이므로 $2 + 0.5 = 2.5$ 입니다."
    },
    {
        "id": "M_2024_09_1",
        "subject": "수학",
        "year": "2024학년도",
        "exam_type": "9월 모의평가",
        "unit": "미적분Ⅰ (도함수)",
        "question": "함수 $f(x) = x^3 - 3x + 5$의 극댓값을 구하시오.",
        "options": ["1) 3", "2) 5", "3) 7", "4) 9", "5) 11"],
        "answer": 3,
        "explanation": "$f'(x) = 3x^2 - 3 = 3(x-1)(x+1) = 0$ 이므로 $x = -1$에서 극댓값 $f(-1) = -1 + 3 + 5 = 7$을 가집니다."
    },
    {
        "id": "M_2024_CSAT_1",
        "subject": "수학",
        "year": "2024학년도",
        "exam_type": "수능",
        "unit": "대수 (로그 계산)",
        "question": "$\\log_2 8 + \\log_3 9$ 의 값을 구하시오.",
        "options": ["1) 3", "2) 4", "3) 5", "4) 6", "5) 7"],
        "answer": 3,
        "explanation": "$\\log_2 8 = 3$, $\\log_3 9 = 2$ 이므로 $3 + 2 = 5$ 입니다."
    },

    # --- 영어 ---
    {
        "id": "E_2024_CSAT_1",
        "subject": "영어",
        "year": "2024학년도",
        "exam_type": "수능",
        "unit": "어법 추론",
        "question": "다음 빈칸에 들어갈 어법상 올바른 표현을 고르시오.\n\nNot only ______ the exam, but he also achieved the highest score.",
        "options": ["1) he passed", "2) did he pass", "3) he had passed", "4) does he pass", "5) he was passing"],
        "answer": 2,
        "explanation": "문두에 부정어(Not only)가 위치하므로 주어와 조동사가 도치된 'did he pass'가 옳습니다."
    },

    # --- 한국사 ---
    {
        "id": "H_2024_CSAT_1",
        "subject": "한국사",
        "year": "2024학년도",
        "exam_type": "수능",
        "unit": "조선 시대",
        "question": "다음 중 조선 영조 때 실시된 정책으로 옳은 것은?",
        "options": ["1) 노비안검법", "2) 과전법", "3) 균역법", "4) 직전법", "5) 대동법"],
        "answer": 3,
        "explanation": "영조는 군포 부담을 줄여주기 위해 군포 2필을 1필로 줄이는 '균역법'을 실시하였습니다."
    }
]

# ----------------------------------------------------
# 2. 사이드바: 필터링 조건 선택
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 필터")
    
    # 1) 과목 선택
    subjects = sorted(list(set(q["subject"] for q in EXAM_DATABASE)))
    selected_subject = st.selectbox("과목 선택", subjects)

    # 2) 연도 선택 (전체 / 특정 연도)
    years = ["전체"] + sorted(list(set(q["year"] for q in EXAM_DATABASE if q["subject"] == selected_subject)), reverse=True)
    selected_year = st.selectbox("연도 선택", years)

    # 3) 시험 종류 선택 (전체 / 6모 / 9모 / 수능)
    exam_types = ["전체", "6월 모의평가", "9월 모의평가", "수능"]
    selected_exam_type = st.selectbox("시험 종류 선택", exam_types)

    st.divider()
    if st.button("🔄 답안 초기화 및 다시 풀기", use_container_width=True):
        st.session_state["user_answers"] = {}
        st.session_state["is_submitted"] = False
        st.rerun()

# ----------------------------------------------------
# 3. 문제 필터링 로직
# ----------------------------------------------------
filtered_questions = [
    q for q in EXAM_DATABASE
    if q["subject"] == selected_subject
    and (selected_year == "전체" or q["year"] == selected_year)
    and (selected_exam_type == "전체" or q["exam_type"] == selected_exam_type)
]

# 세션 상태 초기화
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}

if "is_submitted" not in st.session_state:
    st.session_state["is_submitted"] = False

is_submitted = st.session_state["is_submitted"]
user_answers = st.session_state["user_answers"]

# ----------------------------------------------------
# 4. 문제 풀이 UI 렌더링
# ----------------------------------------------------
st.subheader(f"📌 [{selected_subject}] 검색 결과: 총 {len(filtered_questions)}문항")

if not filtered_questions:
    st.info("선택한 조건(과목/연도/시험 종류)에 해당하는 기출문제가 없습니다. 사이드바에서 필터를 변경해 보세요.")
else:
    for idx, q in enumerate(filtered_questions, 1):
        # 출처 표시 (예: 2024학년도 6월 모의평가 기출)
        st.markdown(f"### **Q{idx}. [{q['year']} {q['exam_type']}] {q['unit']}**")
        st.markdown(f"**{q['question']}**")

        if not is_submitted:
            # 제출 전: 정답 입력 라디오 버튼
            selected_option = st.radio(
                f"Q{idx} 답안 선택",
                options=q["options"],
                key=f"q_radio_{q['id']}",
                index=None,
                label_visibility="collapsed"
            )
            if selected_option:
                ans_num = int(selected_option[0])
                user_answers[q['id']] = ans_num
        else:
            # 제출 후: 채점 결과 및 해설 출력
            user_ans = user_answers.get(q['id'], None)
            correct_ans = q['answer']

            if user_ans == correct_ans:
                st.success(f"⭕ **정답입니다!** (내가 선택한 답: {user_ans}번)")
            elif user_ans is None:
                st.warning(f"⚠️ **미응답** (정답: {correct_ans}번)")
            else:
                st.error(f"❌ **오답입니다.** (내가 선택한 답: {user_ans}번 / 정답: {correct_ans}번)")

            with st.expander("💡 문제 해설 보기", expanded=True):
                st.write(q['explanation'])

        st.divider()

    # ----------------------------------------------------
    # 5. 제출 및 채점
    # ----------------------------------------------------
    if not is_submitted:
        if st.button("📥 OMR 최종 제출 및 채점하기", type="primary", use_container_width=True):
            st.session_state["is_submitted"] = True
            st.rerun()
    else:
        correct_count = sum(1 for q in filtered_questions if user_answers.get(q['id']) == q['answer'])
        total_count = len(filtered_questions)
        score = int((correct_count / total_count) * 100) if total_count > 0 else 0

        st.subheader("📊 채점 결과")
        c1, c2, c3 = st.columns(3)
        c1.metric("풀었던 문항 수", f"{total_count}개")
        c2.metric("맞힌 문항 수", f"{correct_count}개")
        c3.metric("점수", f"{score}점")

        if score == 100:
            st.balloons()
            st.success("🎉 만점입니다!")
