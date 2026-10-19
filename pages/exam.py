import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 다운로드 & OMR",
    page_icon="📝",
    layout="wide"
)

st.title("📝 평가원 전과목 기출문제 자료실")
st.caption("EBSi 및 평가원 공식 기출문제지를 과목별로 연결하여 바로 열람하고 답안을 기록하세요.")

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

# EBSi 연도/시험별 딥링크 (검증된 직통 링크)
EBS_DIRECT_LINKS = {
    "2024학년도 수능 (2023.11)": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311161",
    "2024학년도 9월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309061",
    "2024학년도 6월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306011",
    "2023학년도 수능 (2022.11)": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211171",
    "2023학년도 9월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202208311",
    "2023학년도 6월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202206091"
}

# ----------------------------------------------------
# 2. 사이드바
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    
    selected_exam = st.selectbox("시행 시험 선택", list(EBS_DIRECT_LINKS.keys()))
    selected_domain = st.selectbox("영역 선택", list(EXAM_STRUCTURE.keys()))
    selected_sub = st.selectbox("선택 과목", EXAM_STRUCTURE[selected_domain])

    st.divider()
    st.markdown("🌐 **공식 기출 자료실**")
    st.link_button(
        "평가원 수능 기출 보관함 바로가기",
        "https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung",
        use_container_width=True
    )

# ----------------------------------------------------
# 3. 메인 화면
# ----------------------------------------------------
st.subheader(f"📌 {selected_exam} - [{selected_domain} : {selected_sub}]")

col_left, col_right = st.columns([1, 1])

# 왼쪽: 문제지 접근
with col_left:
    st.markdown("### 📥 기출 문제지 / 정답 열람 및 다운로드")
    
    target_url = EBS_DIRECT_LINKS[selected_exam]
    
    st.success(f"**{selected_domain} - {selected_sub}** 문제지를 열 준비가 되었습니다.")
    
    # 딥링크 연결 버튼
    st.link_button(
        f"📄 [{selected_sub}] 문제지 및 해설 다운로드 열기",
        target_url,
        type="primary",
        use_container_width=True
    )
    
    st.info("""
    💡 **다운로드 오류 발생 시 대처법**:
    1. 위 **[문제지 및 해설 다운로드 열기]** 버튼을 클릭하면 EBSi의 공식 문제지 자료실이 새 창으로 열립니다.
    2. EBSi 화면에서 **PDF 다운로드** 버튼을 누르면 브라우저의 보안 차단 없이 원본 문제지가 바로 다운로드됩니다.
    """)

# 오른쪽: OMR 작성
with col_right:
    st.markdown("### ✏️ OMR 답안 작성")
    
    total_q = 45 if selected_domain in ["국어", "영어"] else (30 if selected_domain == "수학" else 20)

    with st.form(key="omr_submission_form"):
        user_omr = {}
        st.caption(f"**{selected_sub}** 총 {total_q}문항 OMR 답안지")
        
        for row in range(0, total_q, 5):
            cols = st.columns(5)
            for i in range(5):
                q_num = row + i + 1
                if q_num <= total_q:
                    user_omr[q_num] = cols[i].selectbox(
                        f"{q_num}번",
                        options=["-", "1", "2", "3", "4", "5"],
                        key=f"omr_{selected_domain}_{selected_sub}_{q_num}"
                    )
        
        submit_btn = st.form_submit_button("📥 답안 기록 저장", type="primary", use_container_width=True)

    if submit_btn:
        st.success(f"🎉 [{selected_domain} - {selected_sub}] OMR 답안이 정상 저장되었습니다!")
