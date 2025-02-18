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
    
    # 내 제출 필터링
    my_submissions = df[df['이름'] == st.session_state.current_user['name']]
    
    # 주차별 제출 상태
    st.subheader("🎯 문제별 제출 상태")
    
    all_problems = {p['week']: p['links'][0] for p in problems}  # 문제번호: 문제링크
    submitted_problems = dict(zip(my_submissions['주차'], my_submissions['제출링크']))
    
    # 표 형태로 데이터 준비
    table_data = []
    for prob_num, prob_link in all_problems.items():
        status = "✅" if prob_num in submitted_problems else "❌"
        table_data.append({
            "문제번호": prob_num,
            "상태": status,
            "문제 링크": f'<a href="{prob_link}" target="_blank">문제 보기</a>',
            "풀이 링크": f'<a href="{submitted_problems.get(prob_num, "#")}" target="_blank">풀이 보기</a>' if prob_num in submitted_problems else "-"
        })
    
    # DataFrame 생성 및 표시
    table_df = pd.DataFrame(table_data)
    st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # 통계
    st.subheader("📈 나의 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        submission_rate = (len(my_submissions) / len(all_problems)) * 100
        st.metric("내 제출률", f"{submission_rate:.1f}%")
    
    with col2:
        st.metric("총 제출 문제 수", str(len(my_submissions)))

else:
    st.info("아직 제출한 풀이가 없습니다.")