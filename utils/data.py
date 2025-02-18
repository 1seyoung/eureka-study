from datetime import datetime
from .sheets import get_sheet_data, append_row

def get_problems():
    values = get_sheet_data('Problems', 'A2:E')
    problems = []
    for row in values:
        if len(row) >= 4:
            problems.append({
                'set_number': str(row[0]).strip(),  # 문자열로 변환하여 저장
                'task_name': row[1],
                'link': row[2],
                'description': row[3] if len(row) > 3 else "",
                'date_added': row[4] if len(row) > 4 else ""
            })
    st.write("📌 로드된 문제 데이터:", problems)  # 디버깅용 출력
    return problems

def save_submission(name, problem_set, problem_link, solution_link, group=''):
    """제출 데이터 저장"""
    values = [
        name,
        problem_set,
        problem_link,
        solution_link,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        group
    ]
    return append_row('Submissions', values)

def get_submissions():
    """제출 현황 가져오기"""
    values = get_sheet_data('Submissions', 'A2:F')  # 컬럼 개수 확인
    submissions = []
    for row in values:
        if len(row) >= 6:  # 6개 컬럼이 다 있는 경우만 처리
            submissions.append({
                'name': row[0],           # A열 (이름)
                'problem_set': row[1],    # B열 (문제집 번호)
                'problem_link': row[2],   # C열 (문제 링크)
                'solution_link': row[3],  # D열 (풀이 링크)
                'submit_time': row[4],    # E열 (제출 시간)
                'group': row[5]           # F열 (그룹)
            })
    return submissions