import pandas as pd
from .sheets import get_sheet_data

def load_users():
    """사용자 데이터 로드"""
    values = get_sheet_data('Users', 'A2:E')  # E열까지 읽기
    users = []
    for row in values:
        if len(row) >= 5:  # 5개 필드 체크
            users.append({
                'username': row[0],
                'password': row[1],
                'name': row[2],
                'is_admin': row[3].upper() == 'TRUE',
                'group': row[4]  # 그룹 정보 추가
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