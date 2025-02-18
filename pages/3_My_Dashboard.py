# pages/3_📊_My_Dashboard.py
import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title(f"📊 {st.session_state.current_user['name']}님의 제출 현황")

submissions = get_submissions()
problems = get_problems()

if submissions:
    df = pd.DataFrame(submissions)
    my_submissions = df[df['name'] == st.session_state.current_user['name']]
    
    view_mode = st.radio("보기 모드", ["전체 문제", "특정 문제집"])
    
    if view_mode == "특정 문제집":
        problem_sets = sorted(set(p['set_number'].strip() for p in problems))
        selected_set = st.selectbox(
            "문제집 선택",
            options=problem_sets,
            format_func=lambda x: f"{x}번째 문제집"
        )
        filtered_problems = [p for p in problems if p['set_number'].strip() == selected_set]
        filtered_submissions = my_submissions[my_submissions['problem_set'] == selected_set]
    else:
        filtered_problems = problems
        filtered_submissions = my_submissions
    
    st.subheader("🎯 문제 제출 현황")
    
    submitted_solutions = dict(zip(filtered_submissions['problem_link'], 
                                 filtered_submissions['solution_link']))
    
    table_data = []
    for prob in filtered_problems:
        prob_link = prob['link']
        status = "✅" if prob_link in submitted_solutions else "❌"
        
        table_data.append({
            "문제집": f"{prob['set_number']}번째",
            "상태": status,
            "문제": f'<a href="{prob_link}" target="_blank">문제 보기</a>',
            "풀이": f'<a href="{submitted_solutions[prob_link]}" target="_blank">풀이 보기</a>' if prob_link in submitted_solutions else "-",
            "제출일": filtered_submissions[filtered_submissions['problem_link'] == prob_link]['submit_time'].iloc[0] if prob_link in submitted_solutions else "-"
        })
    
    table_df = pd.DataFrame(table_data)
    st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    st.subheader("📈 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        submission_rate = (len(filtered_submissions) / len(filtered_problems)) * 100
        st.metric("제출률", f"{submission_rate:.1f}%")
    
    with col2:
        st.metric("제출 문제 수", f"{len(filtered_submissions)} / {len(filtered_problems)}")

else:
    st.info("아직 제출한 풀이가 없습니다.")