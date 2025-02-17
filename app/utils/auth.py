import streamlit as st
import pandas as pd
import hashlib
from .config import USERS_FILE, DATA_DIR

def load_users():
    """사용자 데이터 로드"""
    if not USERS_FILE.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        initial_users = {
            'username': ['admin'],
            'password': [hashlib.sha256('admin123'.encode()).hexdigest()],
            'name': ['관리자'],
            'is_admin': [True]
        }
        pd.DataFrame(initial_users).to_csv(USERS_FILE, index=False)
    return pd.read_csv(USERS_FILE)


def verify_user(username, password):
    """사용자 인증"""
    users_df = load_users()
    user = users_df[users_df['username'] == username]
    if not user.empty:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.iloc[0]['password'] == hashed_password:
            return True, user.iloc[0]
    return False, None

def login_page():
    """로그인 페이지"""
    st.title("💻 코딩테스트 스터디 플랫폼")
    
    username = st.text_input("사용자명")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        if username and password:
            success, user = verify_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.session_state.is_admin = user['is_admin']
                st.rerun()
            else:
                st.error("잘못된 사용자명 또는 비밀번호입니다.")
        else:
            st.warning("사용자명과 비밀번호를 모두 입력해주세요.")

def check_login():
    """로그인 상태 확인"""
    if not st.session_state.logged_in:
        st.error("로그인이 필요합니다.")
        st.stop()

def add_user(username, password, name, is_admin=False):
    """새 사용자 추가"""
    users_df = load_users()
    if username in users_df['username'].values:
        return False, "이미 존재하는 사용자명입니다."
    
    new_user = pd.DataFrame({
        'username': [username],
        'password': [hashlib.sha256(password.encode()).hexdigest()],
        'name': [name],
        'is_admin': [is_admin]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv('users.csv', index=False)
    return True, "사용자가 추가되었습니다."

def user_management():
    """사용자 관리 페이지"""
    st.header("👥 사용자 관리")
    
    users_df = load_users()
    st.subheader("현재 사용자 목록")
    st.dataframe(users_df[['username', 'name', 'is_admin']], use_container_width=True)
    
    st.subheader("새 사용자 추가")
    col1, col2 = st.columns(2)
    with col1:
        new_username = st.text_input("사용자명")
        new_password = st.text_input("비밀번호", type="password")
    with col2:
        new_name = st.text_input("이름")
        new_is_admin = st.checkbox("관리자 권한")
    
    if st.button("사용자 추가"):
        if new_username and new_password and new_name:
            success, message = add_user(new_username, new_password, new_name, new_is_admin)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        else:
            st.warning("모든 필드를 입력해주세요.")