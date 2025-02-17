# utils/auth.py
import pandas as pd
from .sheets import get_sheet_data  # .을 추가하여 같은 디렉토리의 모듈임을 명시

def load_users():
    """사용자 데이터 로드"""
    values = get_sheet_data('Users', 'A2:D')
    users = []
    for row in values:
        if len(row) >= 4:
            users.append({
                'username': row[0],
                'password': row[1],
                'name': row[2],
                'is_admin': row[3].upper() == 'TRUE'
            })
    return pd.DataFrame(users)

def verify_user(username, password):
    """사용자 인증"""
    users_df = load_users()
    user = users_df[users_df['username'] == username]
    if not user.empty:
        if user.iloc[0]['password'] == password:
            return True, user.iloc[0]
    return False, None