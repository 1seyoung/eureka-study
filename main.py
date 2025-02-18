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
    st.title("💻 코딩테스트 스터디 플랫폼")
    
    username = st.text_input("사용자명")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
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
        st.sidebar.title(f"👋 {st.session_state.current_user['name']}님")
        if st.sidebar.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

if __name__ == "__main__":
    main()