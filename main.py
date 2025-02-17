import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# 페이지 설정
st.set_page_config(
    page_title="코딩테스트 스터디",
    page_icon="💻",
    layout="wide"
)

# 초기 상태 설정
if 'submissions' not in st.session_state:
    st.session_state.submissions = []

if 'problems' not in st.session_state:
    # 초기 문제 데이터
    st.session_state.problems = [
        {
            "week": "1주차",
            "links": [
                "https://school.programmers.co.kr/learn/courses/30/lessons/42748",
                "https://school.programmers.co.kr/learn/courses/30/lessons/42840",
                "https://school.programmers.co.kr/learn/courses/30/lessons/42862"
            ],
            "description": "1주차 문제입니다. 정렬, 완전탐색, 그리디 알고리즘 문제를 준비했습니다.\n\n1. K번째수 (정렬)\n2. 모의고사 (완전탐색)\n3. 체육복 (그리디)",
            "date_added": "2024-02-18"
        },
        {
            "week": "2주차",
            "links": [
                "https://school.programmers.co.kr/learn/courses/30/lessons/1845",
                "https://school.programmers.co.kr/learn/courses/30/lessons/42576",
                "https://school.programmers.co.kr/learn/courses/30/lessons/42577"
            ],
            "description": "2주차 문제입니다. 해시 관련 문제들입니다.\n\n1. 폰켓몬\n2. 완주하지 못한 선수\n3. 전화번호 목록",
            "date_added": "2024-02-18"
        }
    ]

def save_problems():
    """문제 목록을 JSON 파일로 저장"""
    with open('problems.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.problems, f, ensure_ascii=False, indent=2)

def save_submission(name, problem_week, solution_link):
    """제출 정보를 저장"""
    submission_info = {
        "이름": name,
        "주차": problem_week,
        "제출링크": solution_link,
        "제출시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.submissions.append(submission_info)
    
    # CSV 파일로 저장
    df = pd.DataFrame(st.session_state.submissions)
    df.to_csv('submissions.csv', index=False, encoding='utf-8')

def main():
    st.title("💻 코딩테스트 스터디 플랫폼")
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🎯 이번주 문제", "📝 문제 풀이 제출", "📊 제출 현황"])
    
    # 이번주 문제 탭
    with tab1:
        st.header("이번주 코딩테스트 문제")
        
        # 모든 주차 문제 보기
        show_all = st.checkbox("모든 주차 문제 보기")
        
        # 최신 문제 표시
        if st.session_state.problems:
            latest_problem = st.session_state.problems[-1]
            st.subheader(f"📌 {latest_problem['week']} 문제")
            st.write(f"등록일: {latest_problem['date_added']}")
            
            if latest_problem['description']:
                st.write(latest_problem['description'])
            
            st.write("문제 링크:")
            for i, link in enumerate(latest_problem['links'], 1):
                st.markdown(f"{i}. [{link}]({link})")
        else:
            st.info("등록된 문제가 없습니다.")
    
    # 문제 풀이 제출 탭
    with tab2:
        st.header("문제 풀이 제출")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_name = st.text_input("이름")
            submit_week = st.selectbox(
                "주차 선택",
                [p['week'] for p in st.session_state.problems] if st.session_state.problems else ["1주차"]
            )
            submit_link = st.text_input("풀이 링크 (노션, 깃허브 등)")
            
            if st.button("제출하기"):
                if submit_name and submit_link:
                    save_submission(submit_name, submit_week, submit_link)
                    st.success("성공적으로 제출되었습니다!")
                else:
                    st.warning("이름과 링크를 모두 입력해주세요.")
    
    # 제출 현황 탭
    with tab3:
        st.header("제출 현황")
        if st.session_state.submissions:
            df = pd.DataFrame(st.session_state.submissions)
            st.dataframe(df, use_container_width=True)
            
            # 통계
            st.subheader("📊 통계")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("총 제출 수", len(st.session_state.submissions))
            
            with col2:
                unique_students = len(set([s["이름"] for s in st.session_state.submissions]))
                st.metric("참여 학생 수", unique_students)
        else:
            st.info("아직 제출된 풀이가 없습니다.")

if __name__ == "__main__":
    main()