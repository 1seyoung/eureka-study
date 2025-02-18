import streamlit as st
import sys
import os
from utils.auth import verify_user
from utils.data import get_problems

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("🎯 이번주 문제")

# 모든 주차 문제 보기 옵션
show_all = st.checkbox("모든 주차 문제 보기")

problems = get_problems()
if show_all:
    # 모든 주차 문제 표시
    for problem in reversed(problems):
        st.subheader(f"📌 {problem['week']} 문제")
        st.write(f"등록일: {problem['date_added']}")
        st.write(problem['description'])
        st.write("문제 링크:")
        for i, link in enumerate(problem['links'], 1):
            st.markdown(f"{i}. [{link}]({link})")
        st.divider()
else:
    # 최신 문제만 표시
    if problems:
        latest = problems[-1]
        st.subheader(f"📌 {latest['week']} 문제")
        st.write(f"등록일: {latest['date_added']}")
        st.write(latest['description'])
        st.write("문제 링크:")
        for i, link in enumerate(latest['links'], 1):
            st.markdown(f"{i}. [{link}]({link})")