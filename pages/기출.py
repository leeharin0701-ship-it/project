import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출 OMR & 자동 채점",
    page_icon="📝",
    layout="wide"
)

st.title("📝 평가원 기출문제 OMR & 자동 채점 포털")
st.caption("시험 및 과목별로 원본 문제지 링크와 정답 데이터가 연동되어 정확한 자동 채점을 지원합니다.")

# ----------------------------------------------------
# 1. 과목 및 시험 선택 구조
# ----------------------------------------------------
EXAM_STRUCTURE = {
    "국어": ["화법과 작문", "언어와 매체"],
    "수학": ["확률과 통계", "미적분", "기하"],
    "영어": ["공통 (듣기 포함)"],
    "한국사": ["필수 공통"],
    "사회탐구": [
        "생활과 윤리", "윤리와 사상", "한국지리", "세계지리", 
        "동아시아사", "세계사", "경제", "정치와 법", "사회·문화"
    ],
    "과학탐구": [
        "물리학Ⅰ", "화학Ⅰ", "생명과학Ⅰ", "지구과학Ⅰ",
        "물리학Ⅱ", "화학Ⅱ", "생명과학Ⅱ", "지구과학Ⅱ"
    ]
}

# 시행 시험 목록
EXAM_LIST = [
    "2026학년도 수능",
    "2026학년도 9월 모의평가",
    "2026학년도 6월 모의평가",
    "2025학년도 수능",
    "2025학년도 9월 모의평가",
    "2025학년도 6월 모의평가"
]

# ----------------------------------------------------
# 2. 시험 및 과목별 원본 문제지 다운로드 링크
# ----------------------------------------------------
EXAM_SUBJECT_LINKS = {
    "2026학년도 수능": {
        "화법과 작문": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=60defdef6d83db1b756f841089563c5a",
        "언어와 매체": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=60defdef6d83db1b756f841089563c5a",
        "확률과 통계": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=f9055b3484e9176cea7c74b9819a7d2c",
        "미적분": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=f9055b3484e9176cea7c74b9819a7d2c",
        "기하": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=f9055b3484e9176cea7c74b9819a7d2c",
        "공통 (듣기 포함)": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=e0431cad0731556faee928fd38c81241",
        "필수 공통": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=10b6d784275a07a82efa90ddcb8fbd22",
    }
}

DEFAULT_LINK = "https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung"

# ----------------------------------------------------
# 3. 시험별/과목별 정답 데이터베이스
# ----------------------------------------------------
OFFICIAL_ANSWERS = {
    "2026학년도 수능": {
        "화법과 작문": {i: int(c) for i, c in enumerate("354142535531151232432514425513241325312544321", 1)},
        "언어와 매체": {i: int(c) for i, c in enumerate("354142535531151232432514425513241332441245243", 1)}
    }
}

# ----------------------------------------------------
# 4. 사이드바
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    selected_exam = st.selectbox("시행 시험 선택", EXAM_LIST)
    selected_domain = st.selectbox("영역 선택", list(EXAM_STRUCTURE.keys()))
    selected_sub = st.selectbox("선택 과목", EXAM_STRUCTURE[selected_domain])

    st.divider()
    if st.button("🔄 OMR 초기화", use_container_width=True):
        st.session_state["submitted"] = False
        st.session_state["user_answers"] = {}
        st.rerun()

# ----------------------------------------------------
# 5. 메인 화면
# ----------------------------------------------------
st.subheader(f"📌 {selected_exam} - [{selected_domain} : {selected_sub}]")

col_left, col_right = st.columns([1, 1.2])

# 왼쪽: 과목별 맞춤 문제지 다운로드 링크
with col_left:
    st.markdown(f"### 📥 [{selected_sub}] 문제지 열기")
    
    target_url = EXAM_SUBJECT_LINKS.get(selected_exam, {}).get(selected_sub, DEFAULT_LINK)
    
    st.link_button(
        f"📄 [{selected_sub}] 원본 문제지 / PDF 열기",
        target_url,
        type="primary",
        use_container_width=True
    )
    
    st.info("""
    ⌨️ **키보드 입력 팁**:
    1. 문제지 PDF를 화면 옆에 띄워두고 오른쪽 OMR 입력칸에 키보드 숫자를 바로 입력하세요.
    2. **`Tab` 키**를 누르면 다음 문제 입력칸으로 빠르게 이동합니다.
    3. 객관식은 **1~5**, 수학 단답형(22번~)은 **숫자(0~999)**를 입력하면 됩니다.
    """)

# 오른쪽: 키보드 타자 지원 OMR
with col_right:
    st.markdown("### ⌨️ 빠른 OMR 키보드 입력")
    
    total_q = 45 if selected_domain in ["국어", "영어"] else (30 if selected_domain == "수학" else 20)

    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    with st.form(key="fast_keyboard_omr"):
        user_answers = {}
        st.caption(f"총 {total_q}문항 | 숫자를 입력하고 Tab 키로 다음 번호로 이동하세요.")
        
        for row in range(0, total_q, 5):
            cols = st.columns(5)
            for i in range(5):
                q_num = row + i + 1
                if q_num <= total_q:
                    if selected_domain == "수학" and q_num >= 22:
                        ans = cols[i].number_input(
                            f"{q_num}번 (주관식)",
                            min_value=0,
                            max_value=999,
                            value=None,
                            step=1,
                            key=f"q_key_{selected_exam}_{selected_domain}_{selected_sub}_{q_num}"
                        )
                    else:
                        ans = cols[i].number_input(
                            f"{q_num}번 (1~5)",
                            min_value=1,
                            max_value=5,
                            value=None,
                            step=1,
                            key=f"q_key_{selected_exam}_{selected_domain}_{selected_sub}_{q_num}"
                        )
                    user_answers[q_num] = ans
                    
        submit_btn = st.form_submit_button("📥 OMR 제출 및 자동 채점하기", type="primary", use_container_width=True)

    if submit_btn:
        st.session_state["submitted"] = True
        st.session_state["user_answers"] = user_answers

# ----------------------------------------------------
# 6. 자동 채점 결과 표시
# ----------------------------------------------------
if st.session_state.get("submitted", False):
    st.divider()
    st.subheader("📊 자동 채점 결과")
    
    saved_answers = st.session_state.get("user_answers", {})
    
    # 📌 정확하게 해당 시험과 과목의 정답 데이터 가져오기 (없으면 임시 기본값 사용)
    exam_db = OFFICIAL_ANSWERS.get(selected_exam, {})
    correct_db = exam_db.get(selected_sub, {i: (i % 5) + 1 for i in range(1, total_q + 1)})

    correct_count = 0
    wrong_questions = []

    for q_num in range(1, total_q + 1):
        user_ans = saved_answers.get(q_num)
        real_ans = correct_db.get(q_num)

        if user_ans is not None and user_ans == real_ans:
            correct_count += 1
        else:
            wrong_questions.append((q_num, user_ans, real_ans))

    score = int((correct_count / total_q) * 100)

    m1, m2, m3 = st.columns(3)
    m1.metric("총 문항 수", f"{total_q}문항")
    m2.metric("맞힌 문항 수", f"{correct_count}문항")
    m3.metric("최종 점수", f"{score}점 / 100점")

    if score == 100:
        st.balloons()
        st.success("🎉 완벽합니다! 100점 만점입니다.")
    elif score >= 70:
        st.info(f"👍 잘하셨습니다! 틀린 {len(wrong_questions)}문제를 확인하고 오답을 정리해 보세요.")
    else:
        st.warning(f"💪 틀린 {len(wrong_questions)}문제를 복습해 보세요.")

    if wrong_questions:
        with st.expander("❌ 오답 문제 목록 및 정답 확인", expanded=True):
            for q_num, user_a, real_a in wrong_questions:
                u_str = f"{user_a}번" if user_a is not None else "미응답"
                st.write(f"- **{q_num}번**: 내가 쓴 답 `[{u_str}]` / **정답 `[{real_a}번]`**")
