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
        set_num = str(problem['set_number']).strip()  # 숫자라도 문자열 변환
        if set_num not in problem_sets:
            problem_sets[set_num] = {
                'problems': [],  # 문제 정보를 리스트로 저장
                'description': problem.get('description', ''),  # 설명 추가
                'date_added': problem['date_added']
            }
        
        # 문제 정보 추가 (이름 + 링크)
        problem_sets[set_num]['problems'].append({
            'name': problem['task_name'],
            'link': problem['link']
        })
    
    # 문제집 선택 드롭다운
    selected_set = st.selectbox(
        "📚 문제집 선택",
        options=sorted(problem_sets.keys()),
        format_func=lambda x: f"{x}번째 문제집"
    )
    
    # 선택된 문제집 표시
    if selected_set in problem_sets:
        st.header(f"📚 {selected_set}번째 문제집")
        st.write(f"📅 등록일: {problem_sets[selected_set]['date_added']}")
        
        # 설명이 있으면 표시
        if problem_sets[selected_set]['description']:
            st.write(f"📝 {problem_sets[selected_set]['description']}")
        
        # 문제 리스트 테이블 형식으로 표시
        st.subheader("📝 문제 목록")
        table_data = []
        for problem in problem_sets[selected_set]['problems']:
            table_data.append({
                "문제 이름": problem['name'],
                "문제 링크": f'<a href="{problem["link"]}" target="_blank">문제 보기</a>'
            })

        st.write(pd.DataFrame(table_data).to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("등록된 문제가 없습니다.")