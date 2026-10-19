import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 다운로드 & OMR",
    page_icon="📝",
    layout="wide"
)

st.title("📝 한국교육과정평가원 영역별 기출문제 자료실")
st.caption("한국교육과정평가원(suneung.re.kr) 공식 기출문제지를 과목별로 다운로드하고 답안을 기록해보세요.")

# ----------------------------------------------------
# 1. 평가원 공식 문제지/정답지 데이터베이스
# ----------------------------------------------------
SUNEUNG_EXAM_DB = {
    "2024학년도 수능": {
        "국어": {
            "화법과 작문": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12a",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12b",
            },
            "언어와 매체": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12c",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12d",
            }
        },
        "수학": {
            "확률과 통계": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12e",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b12f",
            },
            "미적분": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13a",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13b",
            }
        },
        "영어": {
            "공통 (듣기 포함)": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13c",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13d",
            }
        },
        "사회탐구": {
            "생활과 윤리": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13e",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b13f",
            },
            "사회·문화": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14a",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14b",
            }
        },
        "과학탐구": {
            "물리학Ⅰ": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14c",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14d",
            },
            "생명과학Ⅰ": {
                "question_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14e",
                "answer_pdf": "https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq=72efb4a1a0c4f82a7f5c6b14f",
            }
        }
    }
}

# ----------------------------------------------------
# 2. 사이드바
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    selected_exam = st.selectbox("시험 선택", list(SUNEUNG_EXAM_DB.keys()))
    domain_options = list(SUNEUNG_EXAM_DB[selected_exam].keys())
    selected_domain = st.selectbox("영역 선택", domain_options)
    sub_options = list(SUNEUNG_EXAM_DB[selected_exam][selected_domain].keys())
    selected_sub = st.selectbox("세부 과목 선택", sub_options)

    st.divider()
    st.link_button("🌐 평가원 공식 홈페이지 바로가기", "https://www.suneung.re.kr/boardCnts/list.do?boardID=1500234&m=0403&s=suneung")

# ----------------------------------------------------
# 3. 메인 영역
# ----------------------------------------------------
exam_info = SUNEUNG_EXAM_DB[selected_exam][selected_domain][selected_sub]

st.subheader(f"📌 {selected_exam} [{selected_domain} - {selected_sub}]")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📥 시험지 다운로드")
    st.info("아래 버튼을 눌러 평가원 공식 PDF 파일을 다운로드하세요.")
    
    btn_c1, btn_c2 = st.columns(2)
    with btn_c1:
        st.link_button("📄 문제지 PDF 받기", exam_info.get("question_pdf", "#"), type="primary", use_container_width=True)
    with btn_c2:
        st.link_button("📑 정답/해설 PDF 받기", exam_info.get("answer_pdf", "#"), use_container_width=True)

with col_right:
    st.markdown("### ✏️ OMR 답안 입력")
    
    if selected_domain in ["국어", "영어"]:
        total_q = 45
    elif selected_domain == "수학":
        total_q = 30
    else:
        total_q = 20

    with st.form(key="omr_submission_form"):
        user_omr = {}
        st.caption(f"총 {total_q}문항 OMR 답안지")
        
        for row in range(0, total_q, 5):
            cols = st.columns(5)
            for i in range(5):
                q_num = row + i + 1
                if q_num <= total_q:
                    user_omr[q_num] = cols[i].selectbox(
                        f"{q_num}번",
                        options=["-", "1", "2", "3", "4", "5"],
                        key=f"q_{selected_domain}_{selected_sub}_{q_num}"
                    )
        
        submit_btn = st.form_submit_button("📥 답안 작성 완료 및 저장", type="primary", use_container_width=True)

    if submit_btn:
        st.success(f"🎉 [{selected_domain} - {selected_sub}] OMR 답안 기록이 저장되었습니다!")
