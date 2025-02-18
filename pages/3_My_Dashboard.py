import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems
import plotly.express as px

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
    st.subheader("🎯 주차별 제출 상태")
    
    all_weeks = [p['week'] for p in problems]
    submitted_weeks = my_submissions['주차'].unique()
    
    # 상태 표시를 위한 데이터프레임 생성
    status_data = []
    for week in all_weeks:
        status = "✅ 제출" if week in submitted_weeks else "❌ 미제출"
        link = my_submissions[my_submissions['주차'] == week]['제출링크'].iloc[0] if week in submitted_weeks else ""
        status_data.append({"주차": week, "상태": status, "링크": link})
    
    # 깔끔한 표 형태로 표시
    for _, row in pd.DataFrame(status_data).iterrows():
        cols = st.columns([2, 2, 6])
        with cols[0]:
            st.write(row['주차'])
        with cols[1]:
            st.write(row['상태'])
        with cols[2]:
            if row['링크']:
                st.write(f"[풀이 링크]({row['링크']})")
    
    # 내 통계
    st.subheader("📈 나의 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        submission_rate = (len(my_submissions) / len(all_weeks)) * 100
        st.metric("내 제출률", f"{submission_rate:.1f}%")
    
    with col2:
        st.metric("총 제출 문제 수", len(my_submissions))

else:
    st.info("아직 제출한 풀이가 없습니다.")