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
    # 문제집 번호 추출 및 정렬 (단순 문자열 정렬)
    problem_sets = sorted(set(p['week'].strip() for p in problems))
    
    submit_week = st.selectbox(
        "문제집 선택",
        options=problem_sets,
        format_func=lambda x: f"{x}째 문제집"
    )

    submit_link = st.text_input("풀이 링크 (노션, 깃허브 등)")

    if st.button("제출하기"):
        if submit_link:
            save_submission(
                st.session_state.current_user['name'],
                submit_week,
                submit_link,
                st.session_state.current_user.get('group', '')
            )
            st.success("성공적으로 제출되었습니다!")
        else:
            st.warning("링크를 입력해주세요.")
else:
    st.info("등록된 문제가 없습니다.")