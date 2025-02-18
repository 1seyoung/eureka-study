# pages/2_📝_Submit.py
import streamlit as st
from utils.data import save_submission, get_problems

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("📝 문제 풀이 제출")

problems = get_problems()
if problems:
    # 문제집 목록 가져오기
    problem_sets = sorted(set(str(p['set_number']).strip() for p in problems))
    
    selected_set = st.selectbox(
        "📚 문제집 선택",
        options=problem_sets,
        format_func=lambda x: f"{x}번째 문제집"
    )

    # 선택한 문제집에 속한 문제들 가져오기
    selected_problems = [
        {"name": p['task_name'], "link": p['link']}
        for p in problems if str(p['set_number']).strip() == selected_set
    ]

    # 문제 선택 (문제 이름 + 링크)
    selected_problem = st.selectbox(
        "📝 문제 선택",
        options=selected_problems,
        format_func=lambda p: f"{p['name']} ({p['link']})"
    )

    solution_link = st.text_input("📎 풀이 링크 (노션, 깃허브 등)")

    if st.button("제출하기"):
        if solution_link:
            save_submission(
                name=st.session_state.current_user['name'],
                problem_set=selected_set,
                problem_link=selected_problem['link'],
                solution_link=solution_link,
                group=st.session_state.current_user.get('group', '')
            )
            st.success("✅ 성공적으로 제출되었습니다!")
        else:
            st.warning("⚠ 풀이 링크를 입력해주세요.")
else:
    st.info("⚠ 등록된 문제가 없습니다.")