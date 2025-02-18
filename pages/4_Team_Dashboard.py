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
    
    # 문제 주차 목록 가져오기 (KeyError 방지)
    if problems:
        first_problem = problems[0]
        st.write("🔍 문제 데이터 확인:", first_problem)  # 컬럼명 디버깅
        
        # 'problem_set'이 없으면 'set_number' 사용
        if 'problem_set' not in first_problem and 'set_number' in first_problem:
            all_problems = [p['set_number'] for p in problems]
        else:
            all_problems = [p['problem_set'] for p in problems]
    else:
        all_problems = []

    # 현재 사용자의 그룹
    current_group = st.session_state.current_user['group']
    
    # 그룹 선택 (관리자만 가능)
    if st.session_state.current_user['is_admin']:
        selected_group = st.selectbox(
            "팀 선택",
            options=['전체'] + sorted(df['group'].unique().tolist())
        )
    else:
        selected_group = current_group
        st.info(f"🏢 소속: {current_group}")
    
    # 선택된 그룹으로 데이터 필터링
    if selected_group != '전체':
        df = df[df['group'] == selected_group]
    
    # 멤버별 제출 현황
    st.subheader("👤 멤버별 제출 현황")
    member_stats = df.groupby(['name', 'group']).size().reset_index()
    member_stats.columns = ['이름', '소속', '제출횟수']
    
    if all_problems:
        member_stats['제출률'] = (member_stats['제출횟수'] / len(all_problems) * 100).round(1)
        member_stats['제출률'] = member_stats['제출률'].astype(str) + '%'
    
    # 제출률로 정렬
    member_stats = member_stats.sort_values('제출횟수', ascending=False)
    
    # 내 행 하이라이트
    def highlight_me(row):
        if row['이름'] == st.session_state.current_user['name']:
            return ['background-color: #90EE90'] * len(row)
        return [''] * len(row)
    
    styled_stats = member_stats.style.apply(highlight_me, axis=1)
    st.dataframe(styled_stats, use_container_width=True)
    
    # 그룹별 통계
    if selected_group == '전체':
        st.subheader("📊 그룹별 통계")
        group_stats = member_stats.groupby('소속').agg({
            '이름': 'count',
            '제출횟수': 'sum'
        }).reset_index()
        group_stats.columns = ['그룹', '멤버 수', '총 제출 수']
        group_stats['평균 제출 수'] = (group_stats['총 제출 수'] / group_stats['멤버 수']).round(1)
        st.dataframe(group_stats, use_container_width=True)
    
    # 전체 통계
    st.subheader("📈 통계")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("총 제출 수", len(df))
    
    with col2:
        total_members = len(member_stats)
        avg_submissions = len(df) / total_members if total_members > 0 else 0
        st.metric("인당 평균 제출 수", f"{avg_submissions:.1f}")
    
    with col3:
        if all_problems:
            current_week = all_problems[-1]  # 가장 최근 주차 가져오기
            current_submissions = len(df[df['problem_set'] == current_week]) if 'problem_set' in df.columns else 0
            st.metric(f"{current_week} 제출 수", current_submissions)
        else:
            st.metric("주차 정보 없음", "N/A")

else:
    st.info("아직 제출된 풀이가 없습니다.")