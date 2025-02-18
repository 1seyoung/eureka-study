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
    total_problems = len(problems) if problems else 1  # 0으로 나누는 오류 방지

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

    # 🏆 팀원별 제출 답안 확인 (화면 전환 기능 추가)
    st.subheader("📖 팀원의 제출 답안 확인")

    # 팀원 선택
    team_members = df['name'].unique().tolist()
    selected_member = st.selectbox("팀원 선택", options=team_members, index=0)

    # 선택된 팀원의 제출 데이터 필터링
    member_submissions = df[df['name'] == selected_member]

    if not member_submissions.empty:
        # 📜 제출된 문제 리스트
        st.markdown(f"### 📝 **{selected_member}님의 제출 목록**")
        
        table_data = []
        for _, row in member_submissions.iterrows():
            table_data.append({
                "문제": f'<a href="{row["problem_link"]}" target="_blank">문제 보기</a>',
                "풀이": f'<a href="{row["solution_link"]}" target="_blank">풀이 보기</a>',
                "제출일": row["submit_time"]
            })

        table_df = pd.DataFrame(table_data)
        st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.info(f"{selected_member}님은 아직 제출한 풀이가 없습니다.")

else:
    st.info("아직 제출된 풀이가 없습니다.")