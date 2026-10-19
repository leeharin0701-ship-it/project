import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="평가원 기출문제 전체 자료실",
    page_icon="📝",
    layout="wide"
)

st.title("📝 평가원 전과목·연도별 기출문제 전체 풀이 및 다운로드")
st.caption("EBSi 및 한국교육과정평가원 공식 출제 6월·9월 모의평가 및 수능 전 문항 문제지/정답/해설지입니다.")

# ----------------------------------------------------
# 1. EBSi / 평가원 공식 기출문제 PDF 및 시험지 링크 DB
# ----------------------------------------------------
KICE_FULL_EXAMS = {
    "2024학년도": {
        "수능 (2023.11 시행)": {
            "국어": {
                "pdf": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002341",
                "answer": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002342",
                "ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311161"
            },
            "수학": {
                "pdf": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002343",
                "answer": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002344",
                "ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311162"
            },
            "영어": {
                "pdf": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002345",
                "answer": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002346",
                "ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311163"
            },
            "한국사": {
                "pdf": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002347",
                "answer": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcAtchFile.ax?fileId=FILE_000000001002348",
                "ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202311164"
            }
        },
        "9월 모의평가 (2023.09 시행)": {
            "국어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309061"},
            "수학": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309062"},
            "영어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309063"},
            "한국사": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202309064"}
        },
        "6월 모의평가 (2023.06 시행)": {
            "국어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306011"},
            "수학": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306012"},
            "영어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306013"},
            "한국사": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202306014"}
        }
    },
    "2023학년도": {
        "수능 (2022.11 시행)": {
            "국어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211171"},
            "수학": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211172"},
            "영어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211173"},
            "한국사": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202211174"}
        },
        "9월 모의평가 (2022.08 시행)": {
            "국어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202208311"},
            "수학": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202208312"},
            "영어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202208313"}
        },
        "6월 모의평가 (2022.06 시행)": {
            "국어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202206091"},
            "수학": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202206092"},
            "영어": {"ebs_url": "https://www.ebsi.co.kr/ebs/xip/xipa/retrievePblcPaperExamInfo.ax?examId=202206093"}
        }
    }
}

# ----------------------------------------------------
# 2. 사이드바 검색 필터
# ----------------------------------------------------
with st.sidebar:
    st.header("🎯 기출문제 선택")
    
    # 연도 선택
    selected_year = st.selectbox("학년도 선택", list(KICE_FULL_EXAMS.keys()))
    
    # 시험 종류 선택 (6모, 9모, 수능)
    exam_options = list(KICE_FULL_EXAMS[selected_year].keys())
    selected_exam = st.selectbox("시험 종류 선택", exam_options)
    
    # 과목 선택
    subject_options = list(KICE_FULL_EXAMS[selected_year][selected_exam].keys())
    selected_subject = st.selectbox("과목 선택", subject_options)

# ----------------------------------------------------
# 3. 선택된 기출문제 시험지 렌더링 및 OMR 입력창
# ----------------------------------------------------
exam_data = KICE_FULL_EXAMS[selected_year][selected_exam][selected_subject]

st.subheader(f"📋 {selected_year} {selected_exam} - [{selected_subject}] 전문항 시험지")

col1, col2 = st.columns([3, 2])

with col1:
    st
