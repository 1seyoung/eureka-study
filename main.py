# main.py
import streamlit as st
from utils.auth import verify_user

st.set_page_config(
    page_title="코딩테스트 스터디",
    page_icon="💻",
    layout="wide"
)

# 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("💻 코딩테스트 스터디 플랫폼")
        
        # card 대신 container 사용
        with st.container():
            st.subheader("로그인")
            username = st.text_input("사용자명")
            password = st.text_input("비밀번호", type="password")
            
            if st.button("로그인", use_container_width=True):
                if username and password:
                    success, user = verify_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user
                        st.rerun()
                    else:
                        st.error("잘못된 사용자명 또는 비밀번호입니다.")
                else:
                    st.warning("사용자명과 비밀번호를 모두 입력해주세요.")

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # 사이드바 설정
        with st.sidebar:
            st.title(f"👋 {st.session_state.current_user['name']}님")
            st.divider()
            
            # 네비게이션 메뉴
            st.markdown("""
            ### 📌 메뉴
            - 🎯 이번주 문제
            - 📝 문제 풀이 제출
            - 📊 나의 제출 현황
            - 👥 팀 전체 현황
            """)
            
            st.divider()
            if st.button("로그아웃", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.rerun()
        
        # 메인 페이지 내용
        st.title("💻 코딩테스트 스터디 플랫폼")
        
        # 시작 페이지 안내
        st.info("""
        왼쪽 사이드바의 메뉴를 이용해주세요:
        
        1. 🎯 이번주 문제: 이번 주 풀어야 할 문제를 확인합니다.
        2. 📝 문제 풀이 제출: 풀이 링크를 제출합니다.
        3. 📊 나의 제출 현황: 내 제출 기록을 확인합니다.
        4. 👥 팀 전체 현황: 팀원들의 전체 현황을 확인합니다.
        """)

if __name__ == "__main__":
    main()