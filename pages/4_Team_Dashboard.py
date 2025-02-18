import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from utils.data import get_submissions, get_problems

# 로그인 체크
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("로그인이 필요합니다.")
    st.stop()

st.title("👥 팀 대시보드")

# 데이터 로드
submissions = get_submissions()
problems = get_problems()

if submissions:
    df = pd.DataFrame(submissions)

    # 현재 사용자의 팀(그룹) 가져오기
    current_group = st.session_state.current_user['group']

    # 🏷️ 탭 UI 추가
    tab1, tab2 = st.tabs(["📊 팀 전체 현황", "📖 팀원의 제출 답안 확인"])

    # 📊 팀 전체 현황 탭
    with tab1:
        st.subheader("📋 팀 전체 제출 현황")
        st.info(f"🏢 **현재 소속 팀:** `{current_group}`")

        # 팀 데이터 필터링
        df = df[df['group'] == current_group]

        # ✅ 날짜별 제출 횟수 집계 (깃허브 잔디용)
        df['submit_time'] = pd.to_datetime(df['submit_time'])
        df['date'] = df['submit_time'].dt.date  # 날짜만 추출
        daily_counts = df.groupby('date').size().reset_index(name='count')

        # 📆 최근 90일 데이터 기준으로 빈 날짜도 포함하도록 보정
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=90)
        date_range = pd.date_range(start=start_date, end=end_date)
        all_dates_df = pd.DataFrame({'date': date_range.date})
        daily_counts = pd.merge(all_dates_df, daily_counts, on='date', how='left').fillna(0)

        # 🔥 깃허브 잔디 스타일 히트맵 생성
        fig, ax = plt.subplots(figsize=(12, 3))
        pivot_df = daily_counts.pivot_table(index=[0], columns='date', values='count', aggfunc='sum')

        sns.heatmap(
            pivot_df,
            cmap="Greens",
            linewidths=0.5,
            linecolor="white",
            cbar=False,
            ax=ax
        )

        # 📌 Streamlit에서 이미지로 출력
        st.subheader("📊 팀원 제출 현황 (깃허브 잔디 스타일)")
        st.pyplot(fig)

        # 📈 팀 통계
        st.subheader("📊 팀 통계")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("총 제출 수", len(df))

        with col2:
            total_members = len(df['name'].unique())
            avg_submissions = len(df) / total_members if total_members > 0 else 0
            st.metric("인당 평균 제출 수", f"{avg_submissions:.1f}")

        with col3:
            total_problems = len(problems) if problems else 1
            st.metric("전체 문제 수", total_problems)

else:
    st.info("아직 제출된 풀이가 없습니다.")