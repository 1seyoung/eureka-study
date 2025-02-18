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
        set_num = problem['week'].strip()  # 공백 제거
        if set_num not in problem_sets:
            problem_sets[set_num] = {
                'links': [],
                'date_added': problem['date_added']
            }
        problem_sets[set_num]['links'].append(problem['links'][0])
    
    # 문제집 선택 드롭다운 (단순 문자열 정렬)
    selected_set = st.selectbox(
        "문제집 선택",
        options=sorted(problem_sets.keys()),
        format_func=lambda x: f"{x}째 문제집"
    )
    
    # 선택된 문제집 표시
    if selected_set in problem_sets:
        st.header(f"📚 {selected_set}째 문제집")
        st.write(f"등록일: {problem_sets[selected_set]['date_added']}")
        
        for i, link in enumerate(problem_sets[selected_set]['links'], 1):
            # 링크의 마지막 부분을 문제 번호로 사용
            problem_number = link.split('/')[-1]
            st.markdown(f"{i}. [프로그래머스 {problem_number}번 문제]({link})")
else:
    st.info("등록된 문제가 없습니다.")