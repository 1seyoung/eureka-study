import streamlit as st
import pandas as pd
from utils.auth import check_login
from utils.data import get_submissions

# 로그인 체크
check_login()

st.title("📊 제출 현황")

submissions = get_submissions()
if submissions:
    df = pd.DataFrame(submissions)
    st.dataframe(df, use_container_width=True)
    
    # 통계
    st.subheader("📈 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("총 제출 수", len(submissions))
    
    with col2:
        unique_students = len(set([s["이름"] for s in submissions]))
        st.metric("참여 학생 수", unique_students)
else:
    st.info("아직 제출된 풀이가 없습니다.")