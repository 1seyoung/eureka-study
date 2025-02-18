import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data import get_submissions, get_problems, save_discussion, get_discussions

# 페이지 설정
st.set_page_config(page_title="📊 글로벌 대시보드", layout="wide")

st.title("🌍 글로벌 대시보드")
st.subheader("소속별 및 개인별 제출 현황을 비교합니다.")

# 로그인 체크 및 사용자 정보 가져오기
if 'current_user' not in st.session_state:
    st.session_state.current_user = {'name': 'Guest', 'group': 'Unknown'}

current_user = st.session_state.current_user
user_name = current_user.get('name', 'Guest')
user_group = current_user.get('group', 'Unknown')

# 데이터 로드
submissions = get_submissions()
problems = get_problems()

def display_discussions(discussion_type, key_prefix):
    """의견 나누기 기능"""
    st.subheader("💬 의견 나누기")
    
    # 저장된 의견 불러오기
    discussions = get_discussions()
    
    # 해당 타입의 의견만 필터링
    filtered_discussions = [d for d in discussions if d['type'] == discussion_type]
    
    if filtered_discussions:
        for d in filtered_discussions:
            author = "익명" if d['anonymous'] == "yes" else f"{d['name']} ({d['group']})"
            with st.container():
                st.markdown(f"""**{author}**  
📌 {d['comment']}  
🕒 {d['timestamp']}""")
                st.markdown("---")
    
    # 의견 입력
    discussion_input = st.text_area("✍️ 내용을 입력하세요:", key=f"{key_prefix}_input")
    anonymous_option = st.checkbox("익명으로 제출", key=f"{key_prefix}_anonymous")

    # 제출 버튼
    if st.button("제출", key=f"{key_prefix}_submit"):
        if discussion_input.strip():
            anonymous = "yes" if anonymous_option else "no"
            save_discussion(user_name, user_group, discussion_input, anonymous, discussion_type)
            st.success("제출되었습니다! 📝")
            st.experimental_rerun()  # 새로고침하여 반영
        else:
            st.warning("내용을 입력하세요.")

if submissions:
    df = pd.DataFrame(submissions)
    problems_df = pd.DataFrame(problems)
    
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
        display_discussions("general", "discussion")
    
    # 🏅 **문제별 베스트 답안 목록**
    with tab4:
        st.subheader("🏅 문제별 베스트 답안 목록")

        # best 필드가 존재하는 문제만 필터링
        if 'best' in problems_df.columns:
            best_solutions = problems_df.dropna(subset=['best'])  # best가 있는 문제만 선택

            if not best_solutions.empty:
                # 베스트 답안 링크 HTML 변환
                best_solutions['문제 이름'] = best_solutions['task_name']
                best_solutions['문제 링크'] = best_solutions['link']
                best_solutions['베스트 답안'] = best_solutions['best'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
                
                # 테이블 출력
                st.write(best_solutions[['문제 이름', '문제 링크', '베스트 답안']].to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("아직 베스트 답안이 없습니다.")
        else:
            st.error("베스트 답안 데이터를 찾을 수 없습니다. 관리자에게 문의하세요.")
else:
    st.info("아직 제출된 풀이가 없습니다.")