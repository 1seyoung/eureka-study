import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from utils.data import get_submissions, get_problems

# 한글 폰트 적용 (Streamlit Cloud 환경 대응)
def set_korean_font():
    plt.rcParams["font.family"] = "sans-serif"  # 기본적으로 사용 가능한 폰트
    plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지

set_korean_font()

# 웹 UI 한글 폰트 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');
    * {
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

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

        # ✅ 날짜 변환 및 팀원별 제출 데이터 정리
        df['submit_time'] = pd.to_datetime(df['submit_time'])
        df['date'] = df['submit_time'].dt.date  # 날짜만 추출

        # 📆 최근 90일 기준 데이터 추출
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=90)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        # ✅ 팀원별 날짜별 제출 횟수 집계
        daily_counts = df.groupby(['name', 'date']).size().reset_index(name='count')

        # 📊 꺾은선 그래프 (Line Plot)으로 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for member in df['name'].unique():
            member_data = daily_counts[daily_counts['name'] == member]
            ax.plot(member_data['date'], member_data['count'], marker='o', linestyle='-', label=member)
        
        ax.set_title("팀원별 제출 현황", fontsize=14)
        ax.set_xlabel("날짜", fontsize=12)
        ax.set_ylabel("제출 횟수", fontsize=12)
        ax.legend(title="팀원")
        ax.grid(True, linestyle='--', alpha=0.6)

        # 📌 Streamlit에서 출력
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

    # 📖 팀원의 제출 답안 확인 탭
    with tab2:
        st.subheader("📖 팀원의 제출 답안 확인")

        # 팀원 선택
        team_members = df['name'].unique().tolist()
        selected_member = st.selectbox("👤 팀원 선택", options=team_members, index=0)

        # 선택된 팀원의 제출 데이터 필터링
        member_submissions = df[df['name'] == selected_member]

        if not member_submissions.empty:
            st.markdown(f"### 📝 **{selected_member}님의 제출 목록**")

            # 📌 문제 데이터프레임을 사용해 문제 정보 매칭
            problems_df = pd.DataFrame(problems)

            # 제출된 문제와 문제 정보 병합
            merged_df = pd.merge(member_submissions, problems_df, left_on="problem_link", right_on="link", how="left")

            # 📜 테이블 정리
            table_data = []
            for _, row in merged_df.iterrows():
                table_data.append({
                    "문제집": f"{row['set_number']}번째",
                    "문제 이름": row["task_name"],
                    "설명": row["description"],
                    "문제 링크": f'<a href="{row["problem_link"]}" target="_blank">문제 보기</a>',
                    "풀이 링크": f'<a href="{row["solution_link"]}" target="_blank">풀이 보기</a>',
                    "제출일": row["submit_time"]
                })

            # 🖥️ UI 개선: `st.dataframe()` 대신 HTML 테이블 사용
            table_df = pd.DataFrame(table_data)
            st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info(f"{selected_member}님은 아직 제출한 풀이가 없습니다.")

else:
    st.info("아직 제출된 풀이가 없습니다.")