import streamlit as st
import pandas as pd
from utils.data import get_submissions, get_problems

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
    my_submissions = df[df['name'] == st.session_state.current_user['name']]
    
    # 🏷️ 보기 모드 탭 추가
    tab1, tab2 = st.tabs(["📋 전체 문제 보기", "📚 문제집별 보기"])

    with tab1:  # 전체 문제 보기
        st.subheader("📋 전체 문제 제출 현황")

        # ✅ "전체 문제 보기"에서는 절대 변경되지 않는 문제 리스트 사용!
        all_problems = problems  # 모든 문제 가져오기
        all_submissions = my_submissions  # 모든 제출 데이터

        # ✅ 테이블 데이터 생성 (전체 문제 기준)
        table_data = []
        for prob in all_problems:
            prob_link = prob['link'].strip()
            status = "✅" if prob_link in all_submissions['problem_link'].values else "❌"
            
            table_data.append({
                "문제집": f"{prob['set_number']}번째",
                "문제 이름": prob['task_name'],
                "상태": status,
                "문제 링크": f'<a href="{prob_link}" target="_blank">문제 보기</a>',
                "풀이 링크": "-",
                "제출일": "-"
            })
        
        # ✅ 테이블 출력
        table_df = pd.DataFrame(table_data)
        st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab2:  # 문제집별 보기
        st.subheader("📚 문제집별 제출 현황")

        # ✅ 문제집 목록 가져오기
        problem_sets = sorted(set(str(p['set_number']).strip() for p in problems))
        
        selected_set = st.selectbox(
            "📖 문제집 선택",
            options=problem_sets,
            format_func=lambda x: f"{x}번째 문제집"
        )

        # ✅ 문제집별 보기에서는 `filtered_problems` 사용 (독립 변수!)
        filtered_problems = [p for p in problems if str(p['set_number']).strip() == selected_set]

        # ✅ 해당 문제집의 제출 데이터 필터링
        filtered_submissions = my_submissions[my_submissions['problem_set'] == selected_set]

        # ✅ 제출된 풀이 매핑 (문제집별 전용)
        submitted_solutions = dict(zip(filtered_submissions['problem_link'].str.strip(), 
                                       filtered_submissions['solution_link'].str.strip()))

        # ✅ 문제집별 테이블 데이터 생성
        table_data = []
        for prob in filtered_problems:
            prob_link = prob['link'].strip()
            status = "✅" if prob_link in submitted_solutions else "❌"

            table_data.append({
                "문제집": f"{prob['set_number']}번째",
                "문제 이름": prob['task_name'],
                "상태": status,
                "문제 링크": f'<a href="{prob_link}" target="_blank">문제 보기</a>',
                "풀이 링크": f'<a href="{submitted_solutions[prob_link]}" target="_blank">풀이 보기</a>' if prob_link in submitted_solutions else "-",
                "제출일": filtered_submissions[filtered_submissions['problem_link'].str.strip() == prob_link]['submit_time'].iloc[0] if prob_link in submitted_solutions else "-"
            })

        # ✅ 테이블 출력
        table_df = pd.DataFrame(table_data)
        st.write(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("아직 제출한 풀이가 없습니다.")