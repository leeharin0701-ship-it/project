import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 다운로드 & OMR",
    page_icon="📝",
    layout="wide"
)

# Custom CSS로 OMR 스타일링 (동그라미 라디오 버튼 가로 배치 및 보기 깔끔하게 처리)
st.markdown("""
<style>
    /* OMR 문항 번호와 라디오 버튼 간격 및 디자인 제어 */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    div[data-testid="stForm"] {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 평가원 전과목 기출문제 자료실 & OMR")
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

# EBSi 연도/시험별 직통 딥링크
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

col_left, col_right = st.columns([1, 1.2])

# 왼쪽: 문제지 다운로드 링크
with col_left:
    st.markdown("### 📥 기출 문제지 / 정답 열람")
    
    target_url = EBS_DIRECT_LINKS[selected_exam]
    
    st.success(f"**{selected_domain} - {selected_sub}** 문제지를 열 준비가 되었습니다.")
    
    st.link_button(
        f"📄 [{selected_sub}] 문제지 및 해설 다운로드 열기",
        target_url,
        type="primary",
        use_container_width=True
    )
    
    st.info("""
    💡 **이용 가이드**:
    1. 위 버튼을 누르면 EBSi의 공식 문제지/해설지 열람 페이지가 새 창으로 연결됩니다.
    2. 문제지를 보면서 오른쪽에 실제 수능 OMR 카드처럼 답안을 마킹해 보세요.
    3. **수학 영역**의 22번~30번 문항은 주관식(서답형) 숫자를 직접 입력할 수 있습니다.
    """)

# 오른쪽: 실제 스타일 OMR 카드
with col_right:
    st.markdown("### 🏷️ OMR 답안지")
    
    total_q = 45 if selected_domain in ["국어", "영어"] else (30 if selected_domain == "수학" else 20)

    with st.form(key="real_omr_form"):
        user_omr = {}
        st.caption(f"**[{selected_domain} - {selected_sub}]** 총 {total_q}문항")
        
        # OMR 카드 레이아웃 구성
        for q_num in range(1, total_q + 1):
            c_num, c_marks = st.columns([1, 4])
            
            # 수학 서답형 문항 (22번~30번) 처리
            if selected_domain == "수학" and q_num >= 22:
                with c_num:
                    st.markdown(f"**{q_num}번** *(주관식)*")
                with c_marks:
                    user_omr[q_num] = st.number_input(
                        f"{q_num}번 정답 숫자 입력",
                        min_value=0,
                        max_value=999,
                        step=1,
                        key=f"sub_{q_num}",
                        label_visibility="collapsed"
                    )
            # 일반 객관식 문항 (①~⑤ 동그라미)
            else:
                with c_num:
                    st.markdown(f"**{q_num}번**")
                with c_marks:
                    user_omr[q_num] = st.radio(
                        f"{q_num}번 답안",
                        options=["①", "②", "③", "④", "⑤"],
                        key=f"omr_radio_{selected_domain}_{selected_sub}_{q_num}",
                        horizontal=True,
                        index=None,
                        label_visibility="collapsed"
                    )
            
            # 5문제마다 구분선 표시
            if q_num % 5 == 0 and q_num != total_q:
                st.markdown("<hr style='margin: 8px 0; border: 0.5px dashed #ccc;'>", unsafe_allow_html=True)

        st.divider()
        submit_btn = st.form_submit_button("📥 OMR 답안 제출 및 기록 저장", type="primary", use_container_width=True)

    if submit_btn:
        st.success(f"🎉 [{selected_domain} - {selected_sub}] OMR 답안이 정상적으로 제출 및 저장되었습니다!")
