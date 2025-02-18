import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems

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

    # 현재 사용자의 팀(그룹) 가져오기
    current_group = st.session_state.current_user['group']
    st.info(f"🏢 **현재 소속 팀:** `{current_group}`")

    # 팀에 속한 멤버들의 제출 데이터만 필터링
    df = df[df['group'] == current_group]

    # 팀 멤버별 제출 현황 집계
    member_stats = df.groupby(['name']).size().reset_index()
    member_stats.columns = ['이름', '제출 횟수']

    # 문제집 개수 가져오기
    if problems:
        total_problems = len(problems)
    else:
        total_problems = 1  # 0으로 나누는 오류 방지

    # 제출률 계산
    member_stats['제출률'] = (member_stats['제출 횟수'] / total_problems * 100).round(1)
    member_stats['제출률'] = member_stats['제출률'].astype(str) + '%'

    # 제출 횟수 기준 정렬
    member_stats = member_stats.sort_values('제출 횟수', ascending=False)

    # 내 행 하이라이트 (내 계정의 제출 행 강조)
    def highlight_me(row):
        if row['이름'] == st.session_state.current_user['name']:
            return ['background-color: #90EE90'] * len(row)
        return [''] * len(row)

    styled_stats = member_stats.style.apply(highlight_me, axis=1)

    # 📊 멤버별 제출 현황
    st.subheader("📋 멤버별 제출 현황")
    st.dataframe(styled_stats, use_container_width=True)

    # 📈 팀 통계
    st.subheader("📊 팀 통계")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("총 제출 수", len(df))

    with col2:
        total_members = len(member_stats)
        avg_submissions = len(df) / total_members if total_members > 0 else 0
        st.metric("인당 평균 제출 수", f"{avg_submissions:.1f}")

    with col3:
        st.metric("전체 문제 수", total_problems)

else:
    st.info("아직 제출된 풀이가 없습니다.")