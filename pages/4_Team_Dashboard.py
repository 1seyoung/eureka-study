import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems
import plotly.express as px

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("👥 팀 전체 현황")

# 데이터 로드
submissions = get_submissions()
problems = get_problems()

if submissions:
    df = pd.DataFrame(submissions)
    all_weeks = [p['week'] for p in problems]
    total_members = df['이름'].nunique()
    
    # 주차별 제출률
    st.subheader("📊 주차별 제출 현황")
    weekly_submissions = df.groupby('주차').size()
    
    week_stats = []
    for week in all_weeks:
        submissions_count = weekly_submissions.get(week, 0)
        submission_rate = (submissions_count / total_members) * 100
        week_stats.append({
            "주차": week,
            "제출인원": submissions_count,
            "제출률": f"{submission_rate:.1f}%"
        })
    
    st.dataframe(pd.DataFrame(week_stats), use_container_width=True)
    
    # 멤버별 제출 현황
    st.subheader("👤 멤버별 제출 현황")
    member_stats = df.groupby('이름').size().reset_index()
    member_stats.columns = ['이름', '제출횟수']
    member_stats['제출률'] = (member_stats['제출횟수'] / len(all_weeks) * 100).round(1)
    member_stats['제출률'] = member_stats['제출률'].astype(str) + '%'
    
    # 제출률로 정렬
    member_stats = member_stats.sort_values('제출횟수', ascending=False)
    
    # 현재 사용자 하이라이트
    def highlight_me(row):
        if row['이름'] == st.session_state.current_user['name']:
            return ['background-color: #90EE90'] * len(row)
        return [''] * len(row)
    
    styled_stats = member_stats.style.apply(highlight_me, axis=1)
    st.dataframe(styled_stats, use_container_width=True)
    
    # 전체 통계
    st.subheader("📈 전체 통계")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 제출 수", len(df))
    
    with col2:
        avg_submissions = len(df) / total_members
        st.metric("인당 평균 제출 수", f"{avg_submissions:.1f}")
    
    with col3:
        current_week = all_weeks[-1]
        current_submissions = len(df[df['주차'] == current_week])
        st.metric(f"{current_week} 제출 수", current_submissions)

else:
    st.info("아직 제출된 풀이가 없습니다.")