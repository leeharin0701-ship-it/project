import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출 OMR & 자동 채점",
    page_icon="📝",
    layout="wide"
)

st.title("📝 평가원 기출문제 OMR & 자동 채점 포털")
st.caption("시험 및 과목별로 원본 문제지 링크를 각각 연결하여 바로 다운로드하고 채점하세요.")

# ----------------------------------------------------
# 1. 과목 및 시험 선택 구조
# ----------------------------------------------------
EXAM_STRUCTURE = {
    "국어": ["국어 영역"],
    "수학": ["수학 영역"],
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
# 2. [핵심] 시험 및 과목별 개별 링크 데이터베이스
# ----------------------------------------------------
# 구조: { "시험 이름": { "과목명": "해당 과목 PDF 또는 다운로드 링크" } }
# ※ 아래 링크는 예시이며, 원하시는 과목별 링크(PDF 주소 또는 EBSi/평가원 상세페이지)를 자유롭게 수정·입력하세요.
EXAM_SUBJECT_LINKS = {
    "2026학년도 수능": {
        "국어 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=60defdef6d83db1b756f841089563c5a",
        "수학 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=f9055b3484e9176cea7c74b9819a7d2c",
        "영어 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=e0431cad0731556faee928fd38c81241",
        "한국사": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=10b6d784275a07a82efa90ddcb8fbd22",
        "사회 탐구": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=10b6d784275a07a82efa90ddcb8fbd22", #보류
        "과학 탐구": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=10b6d784275a07a82efa90ddcb8fbd22",
        # 필요한 과목들의 링크를 계속 추가할 수 있습니다.
    },
    "2025학년도 9월 수능": {
         "국어 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=60defdef6d83db1b756f841089563c5a",
        "수학 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=f9055b3484e9176cea7c74b9819a7d2c",
        "영어 영역": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=e0431cad0731556faee928fd38c81241",
        "한국사": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=10b6d784275a07a82efa90ddcb8fbd22",
    }
}




















# 기본 fallback 링크 (등록되지 않은 과목 선택 시 안내용)
DEFAULT_LINK = "https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung"

# ----------------------------------------------------
# 3. 시험별 예시 정답 데이터베이스 (자동 채점용)
# ----------------------------------------------------
OFFICIAL_ANSWERS = {
    "국어": {1: 1, 2: 4, 3: 2, 4: 5, 5: 3, 6: 1, 7: 3, 8: 4, 9: 2, 10: 5, 
             11: 3, 12: 1, 13: 4, 14: 2, 15: 5, 16: 2, 17: 3, 18: 1, 19: 4, 20: 5,
             21: 1, 22: 3, 23: 2, 24: 4, 25: 5, 26: 1, 27: 3, 28: 2, 29: 4, 30: 5,
             31: 2, 32: 1, 33: 4, 34: 3, 35: 5, 36: 1, 37: 2, 38: 4, 39: 3, 40: 5,
             41: 2, 42: 1, 43: 3, 44: 4, 45: 5},
    "수학": {1: 3, 2: 5, 3: 1, 4: 4, 5: 2, 6: 3, 7: 5, 8: 1, 9: 4, 10: 2,
             11: 3, 12: 5, 13: 1, 14: 4, 15: 2, 16: 3, 17: 5, 18: 1, 19: 4, 20: 2,
             21: 3, 22: 15, 23: 3, 24: 12, 25: 8, 26: 27, 27: 5, 28: 16, 29: 84, 30: 125},
    "영어": {i: (i % 5) + 1 for i in range(1, 46)},
    "탐구": {i: (i % 5) + 1 for i in range(1, 21)}
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
        st.session_state["omr_inputs"] = {}
        st.rerun()

# ----------------------------------------------------
# 5. 메인 화면
# ----------------------------------------------------
st.subheader(f"📌 {selected_exam} - [{selected_domain} : {selected_sub}]")

col_left, col_right = st.columns([1, 1.2])

# 왼쪽: 과목별 맞춤 문제지 다운로드 링크
with col_left:
    st.markdown(f"### 📥 [{selected_sub}] 문제지 열기")
    
    # 선택된 시험과 과목에 맞는 링크 가져오기 (없으면 기본 평가원 보관함 링크 제공)
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
                            key=f"q_key_{selected_domain}_{selected_sub}_{q_num}"
                        )
                    else:
                        ans = cols[i].number_input(
                            f"{q_num}번 (1~5)",
                            min_value=1,
                            max_value=5,
                            value=None,
                            step=1,
                            key=f"q_key_{selected_domain}_{selected_sub}_{q_num}"
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
    
    if selected_domain in OFFICIAL_ANSWERS:
        correct_db = OFFICIAL_ANSWERS[selected_domain]
    else:
        correct_db = OFFICIAL_ANSWERS["탐구"]

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
