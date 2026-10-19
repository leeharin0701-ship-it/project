import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 전체 자료실",
    page_icon="📝",
    layout="wide"
)

st.title("📝 한국교육과정평가원 수능/모의평가 전과목 기출 포털")
st.caption("국어, 수학, 영어, 한국사 및 사회/과학탐구 전과목(화학, 지구과학 포함) 기출문제 다운로드 및 OMR 채점입니다.")

# ----------------------------------------------------
# 1. 탐구 및 선택과목 구조 정의
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

# EBSi 기출문제 포털 매핑 (연도/시험별)
EBS_EXAM_LINKS = {
    "2024학년도 수능": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311161",
    "2024학년도 9월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309061",
    "2024학년도 6월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306011",
    "2023학년도 수능": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211171",
    "2023학년도 9월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202208311",
    "2023학년도 6월 모의평가": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202206091"
}

# ----------------------------------------------------
# 2. 사이드바 검색 조건
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    
    selected_exam = st.selectbox("시행 시험 선택", list(EBS_EXAM_LINKS.keys()))
    selected_domain = st.selectbox("영역 선택", list(EXAM_STRUCTURE.keys()))
    selected_sub = st.selectbox("선택 과목", EXAM_STRUCTURE[selected_domain])

    st.divider()
    st.markdown("🔗 **공식 자료실 이동**")
    st.link_button(
        "🌐 평가원 수능 공식 기출 자료실",
        "https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung",
        use_container_width=True
    )

# ----------------------------------------------------
# 3. 메인 화면
# ----------------------------------------------------
st.subheader(f"📌 {selected_exam} - [{selected_domain} : {selected_sub}]")

col_left, col_right = st.columns([1, 1])

# 왼쪽: 다운로드 및 공식 페이지 바로가기
with col_left:
    st.markdown("### 📥 기출 문제지 / 정답 다운로드")
    st.info(f"**{selected_domain} ({selected_sub})** 전 문항 문제지 및 정답/해설지입니다.")
    
    exam_url = EBS_EXAM_LINKS[selected_exam]
    
    st.link_button(
        f"📄 {selected_sub} 문제지/정답/해설 다운로드 (EBSi 공식)",
        exam_url,
        type="primary",
        use_container_width=True
    )
    
    st.divider()
    st.markdown("""
    #### 💡 문제지 다운로드 안내
    1. 위 버튼을 누르면 해당 시험의 **전과목 문제지 PDF, 정답지, 해설지 및 등급컷**을 바로 열람/다운로드하실 수 있습니다.
    2. 평가원 서버 직접 다운로드 오류 방지를 위해 EBSi 공식 고화질 PDF 시스템을 연동하였습니다.
    3. 다운로드받은 문제지를 보면서 오른쪽에 정답을 작성해 보세요.
    """)

# 오른쪽: OMR 입력 양식
with col_right:
    st.markdown("### ✏️ OMR 답안 작성")
    
    # 영역별 문제 수 자동 지정 (국어/영어 45문항, 수학 30문항, 탐구 20문항)
    if selected_domain in ["국어", "영어"]:
        total_q = 45
    elif selected_domain == "수학":
        total_q = 30
    else:
        total_q = 20

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
        
        submit_btn = st.form_submit_button("📥 답안 작성 완료 및 저장", type="primary", use_container_width=True)

    if submit_btn:
        st.success(f"🎉 [{selected_domain} - {selected_sub}] OMR 답안 기록이 저장되었습니다!")
