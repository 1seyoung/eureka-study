# pages/1_🎯_Problems.py
import streamlit as st
from utils.data import get_problems

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("🎯 이번주 문제")

problems = get_problems()
if problems:
    # 문제집 번호로 그룹화
    problem_sets = {}
    for problem in problems:
        set_num = problem['week']  # 'week' 필드를 문제집 번호로 사용
        if set_num not in problem_sets:
            problem_sets[set_num] = {
                'links': [],
                'date_added': problem['date_added']
            }
        problem_sets[set_num]['links'].append(problem['links'][0])
    
    # 문제집 별로 표시
    for set_num, data in problem_sets.items():
        st.header(f"📚 {set_num}번 문제집")
        st.write(f"등록일: {data['date_added']}")
        
        for i, link in enumerate(data['links'], 1):
            st.markdown(f"{i}. [{link}]({link})")
        
        st.divider()
else:
    st.info("등록된 문제가 없습니다.")