import streamlit as st
from app.utils.auth import check_login
from app.utils.data import load_problems

check_login()
st.title("🎯 이번주 문제")

problems = load_problems()
show_all = st.checkbox("모든 주차 문제 보기")

if show_all:
    # 모든 주차 문제 표시
    for problem in reversed(problems):
        st.subheader(f"📌 {problem['week']} 문제")
        st.write(f"등록일: {problem['date_added']}")
        if problem['description']:
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
        if latest['description']:
            st.write(latest['description'])
        st.write("문제 링크:")
        for i, link in enumerate(latest['links'], 1):
            st.markdown(f"{i}. [{link}]({link})")