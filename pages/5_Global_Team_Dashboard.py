import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data import get_submissions, get_problems

# 페이지 설정
st.set_page_config(page_title="📊 글로벌 대시보드", layout="wide")

st.title("🌍 글로벌 대시보드")
st.subheader("소속별 제출 현황을 비교합니다.")

# 데이터 로드
submissions = get_submissions()
problems = get_problems()

if submissions:
    df = pd.DataFrame(submissions)

    # 소속(그룹)별 데이터 집계
    group_stats = df.groupby('group').agg(
        총_제출_수=('name', 'count'),
        멤버_수=('name', 'nunique')
    ).reset_index()

    # 전체 문제 수 계산
    total_problems = len(problems) if problems else 1  # 0 나눗셈 방지

    # 제출률 계산
    group_stats['평균 제출률 (%)'] = ((group_stats['총_제출_수'] / (group_stats['멤버_수'] * total_problems)) * 100).round(1)

    # 제출 수 기준 정렬
    group_stats = group_stats.sort_values(by='총_제출_수', ascending=False)

    # 가장 활발한 팀 & 평균 제출률이 높은 팀 하이라이트
    most_active_team = group_stats.iloc[0]['group'] if not group_stats.empty else "N/A"
    best_submission_team = group_stats.sort_values(by='평균 제출률 (%)', ascending=False).iloc[0]['group'] if not group_stats.empty else "N/A"

    # 🏆 **하이라이트 정보**
    st.markdown(f"🏅 **가장 활발한 팀:** `{most_active_team}` (제출 수 최다)")
    st.markdown(f"📈 **평균 제출률이 가장 높은 팀:** `{best_submission_team}`")

    # 📊 **소속별 제출 통계 표**
    st.subheader("📋 소속별 제출 통계")
    st.dataframe(group_stats, use_container_width=True)

    # 📈 **시각화 (그래프)**
    st.subheader("📊 소속별 제출 통계 시각화")

    col1, col2 = st.columns(2)

    with col1:
        # 팀별 총 제출 수 그래프
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(group_stats['group'], group_stats['총_제출_수'], color='royalblue')
        ax.set_title("소속별 총 제출 수")
        ax.set_ylabel("제출 수")
        ax.set_xticklabels(group_stats['group'], rotation=45, ha='right')
        st.pyplot(fig)

    with col2:
        # 팀별 평균 제출률 그래프
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(group_stats['group'], group_stats['평균 제출률 (%)'], color='darkorange')
        ax.set_title("소속별 평균 제출률")
        ax.set_ylabel("제출률 (%)")
        ax.set_xticklabels(group_stats['group'], rotation=45, ha='right')
        st.pyplot(fig)

else:
    st.info("아직 제출된 풀이가 없습니다.")