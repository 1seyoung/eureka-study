# pages/3_📊_My_Dashboard.py
import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title(f"📊 {st.session_state.current_user['name']}님의 제출 현황")

# 데이터 로드
submissions = get_submissions()
problems = get_problems()

if submissions:
    df = pd.DataFrame(submissions)
    my_submissions = df[df['이름'] == st.session_state.current_user['name']]
    
    # 문제집 선택 옵션
    view_options = ["전체 문제", "특정 문제집"]
    view_mode = st.radio("보기 모드", view_options)
    
    if view_mode == "특정 문제집":
        # 문제집 선택
        problem_sets = sorted(set(p['week'].strip() for p in problems))
        selected_set = st.selectbox(
            "문제집 선택",
            options=problem_sets,
            format_func=lambda x: f"{x}번째 문제집"
        )
        
        # 선택된 문제집의 문제만 필터링
        filtered_problems = {p['week']: p['links'][0] for p in problems if p['week'].strip() == selected_set}
        filtered_submissions = my_submissions[my_submissions['주차'] == selected_set]
    else:
        # 전체 문제
        filtered_problems = {p['week']: p['links'][0] for p in problems}
        filtered_submissions = my_submissions
    
    # 제출 상태 표시
    st.subheader("🎯 문제 제출 현황")
    submitted_problems = dict(zip(filtered_submissions['주차'], filtered_submissions['제출링크']))
    
    # 표 데이터 준비
    table_data = []
    for prob_num, prob_link in filtered_problems.items():
        status = "✅" if prob_num in submitted_problems else "❌"
        table_data.append({
            "문제집": f"{prob_num}번째",
            "상태": status,
            "문제 링크": f'<a href="{prob_link}" target="_blank">문제 보기</a>',
            "풀이 링크": f'<a href="{submitted_problems.get(prob_num, "#")}" target="_blank">풀이 보기</a>' if prob_num in submitted_problems else "-"
        })
    
    # DataFrame 생성 및 표시
    table_df = pd.DataFrame(table_data)
    st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # 통계
    st.subheader("📈 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        submission_rate = (len(filtered_submissions) / len(filtered_problems)) * 100
        st.metric("제출률", f"{submission_rate:.1f}%")
    
    with col2:
        st.metric("제출 문제 수", f"{len(filtered_submissions)} / {len(filtered_problems)}")

else:
    st.info("아직 제출한 풀이가 없습니다.")