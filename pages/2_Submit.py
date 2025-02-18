# pages/2_📝_Submit.py
import streamlit as st
from utils.data import save_submission, get_problems

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("📝 문제 풀이 제출")

problems = get_problems()
if problems:
    # Select problem set
    problem_sets = sorted(set(p['set_number'].strip() for p in problems))
    selected_set = st.selectbox(
        "문제집 선택",
        options=problem_sets,
        format_func=lambda x: f"{x}번째 문제집"
    )

    # Select specific problem
    selected_problems = [p['link'] for p in problems if p['set_number'].strip() == selected_set]
    selected_problem = st.selectbox(
        "문제 선택",
        options=selected_problems,
        format_func=lambda x: f"문제 링크: {x}"
    )

    solution_link = st.text_input("풀이 링크 (노션, 깃허브 등)")

    if st.button("제출하기"):
        if solution_link:
            save_submission(
                name=st.session_state.current_user['name'],
                problem_set=selected_set,
                problem_link=selected_problem,
                solution_link=solution_link,
                group=st.session_state.current_user.get('group', '')
            )
            st.success("성공적으로 제출되었습니다!")
        else:
            st.warning("링크를 입력해주세요.")
else:
    st.info("등록된 문제가 없습니다.")