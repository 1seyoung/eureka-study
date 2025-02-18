# pages/1_🎯_Problems.py
import streamlit as st
from utils.data import get_problems
import pandas as pd

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("🎯 문제집")

problems = get_problems()
if problems:
    # 문제집 이름으로 그룹화
    problem_sets = {}
    for problem in problems:
        set_name = str(problem['set']).strip()  # 문제집 이름으로 그룹화
        if set_name not in problem_sets:
            problem_sets[set_name] = {
                'problems': [],  # 문제 정보를 리스트로 저장
                'date_added': problem['date_added']
            }
        
        # 문제 정보 추가 (이름 + 링크 + 설명)
        problem_sets[set_name]['problems'].append({
            'name': problem['task_name'],
            'link': problem['link'],
            'description': problem.get('description', '')  # 문제 설명 추가
        })
    
    # 문제집 선택 드롭다운
    selected_set = st.selectbox(
        "📚 문제집 선택",
        options=sorted(problem_sets.keys()),
        format_func=lambda x: f"{x}"
    )
    
    # 선택된 문제집 표시
    if selected_set in problem_sets:
        st.header(f"📚 {selected_set}")
        st.write(f"📅 등록일: {problem_sets[selected_set]['date_added']}")
        
        # 문제 리스트 테이블 형식으로 표시
        st.subheader("📝 문제 목록")
        table_data = []
        for problem in problem_sets[selected_set]['problems']:
            table_data.append({
                "문제 이름": problem['name'],
                "문제 설명": problem['description'],
                "문제 링크": f'<a href="{problem["link"]}" target="_blank">문제 보기</a>'
            })

        st.write(pd.DataFrame(table_data).to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("등록된 문제가 없습니다.")
