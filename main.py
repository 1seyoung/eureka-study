# main.py
import streamlit as st
from utils.auth import verify_user

st.set_page_config(
    page_title="백엔드 코딩테스트 스터디",
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
        st.title("💻 백엔드 코딩테스트 스터디 플랫폼")
        
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
            - 🎯 이번주 백엔드 문제
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
        st.title("💻 백엔드 코딩테스트 스터디 플랫폼")
        
        # 시작 페이지 안내
        st.info("""
        왼쪽 사이드바의 메뉴를 이용해주세요:
        
        1. 🎯 이번주 백엔드 문제: 이번 주 풀어야 할 백엔드 중심 문제를 확인합니다.
        2. 📝 문제 풀이 제출: 백엔드 문제 풀이 링크를 제출합니다.
        3. 📊 나의 제출 현황: 내 제출 기록을 확인합니다.
        4. 👥 팀 전체 현황: 팀원들의 전체 현황을 확인합니다.
        """)

        # 📌 백엔드 문제 풀이 제출 가이드
        st.subheader("📝 백엔드 문제 풀이 제출 가이드")
        st.markdown("""
        **제출 양식:** 블로그, 노션 등의 플랫폼을 활용하여 백엔드 문제 풀이를 정리한 후 공유해주세요.
        
        제출 내용은 다음과 같은 형식을 따릅니다:
        
        1. **문제 분석**: 백엔드 문제를 분석하고 핵심 요구사항을 정리합니다.
        2. **아이디어 및 수도코드**: 해결 방안을 아이디어 차원에서 정리하고, 수도코드를 작성합니다.
        3. **코드**: 실제 구현한 코드를 포함합니다.
        4. **제출 결과**: 해당 코드의 실행 결과 및 제출 성공 여부를 기록합니다.
        
        제출 예시:
        - 📄 블로그: [링크 예시](https://example.com)
        - 📄 노션: [링크 예시](https://example.com)
        """)

if __name__ == "__main__":
    main()