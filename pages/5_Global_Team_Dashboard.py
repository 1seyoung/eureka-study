import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems, get_best_solutions

# 페이지 설정
st.set_page_config(page_title="📊 글로벌 대시보드", layout="wide")

st.title("🌍 글로벌 대시보드")
st.subheader("소속별 및 개인별 제출 현황을 비교합니다.")

# 데이터 로드
submissions = get_submissions()
problems = get_problems()
best_solutions = get_best_solutions()

if submissions:
    df = pd.DataFrame(submissions)
    
    # 🏷️ 탭 UI 추가
    tab1, tab2, tab3, tab4 = st.tabs(["📋 소속별 제출 통계", "🏆 개인별 제출 순위", "💬 의견 나누기", "🏅 문제별 베스트 답안"])
    
    # 📋 **소속별 제출 통계**
    with tab1:
        st.subheader("📋 소속별 제출 통계")
        
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

        st.dataframe(group_stats, use_container_width=True)
    
    # 🏆 **개인별 제출 순위**
    with tab2:
        st.subheader("🏆 개인별 제출 순위")
        individual_stats = df.groupby(['name', 'group']).size().reset_index(name='제출 수')
        individual_stats = individual_stats.sort_values(by='제출 수', ascending=False)
        individual_stats['등수'] = range(1, len(individual_stats) + 1)
        st.dataframe(individual_stats[['등수', 'name', 'group', '제출 수']], use_container_width=True)
    
    # 💬 **의견 나누기**
    with tab3:
        st.subheader("💬 의견 나누기")
        discussion = st.text_area("팀원들과 토론할 내용을 입력하세요:")
        if st.button("의견 제출"):
            st.success("의견이 제출되었습니다! 📝")
    
    # 🏅 **문제별 베스트 답안 목록**
    with tab4:
        st.subheader("🏅 문제별 베스트 답안 목록")
        if best_solutions:
            best_df = pd.DataFrame(best_solutions)
            st.dataframe(best_df, use_container_width=True)
        else:
            st.info("아직 베스트 답안이 없습니다.")
else:
    st.info("아직 제출된 풀이가 없습니다.")