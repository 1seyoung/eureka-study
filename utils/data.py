from datetime import datetime
from .sheets import get_sheet_data, append_row

def get_problems():
    """문제 목록 가져오기"""
    values = get_sheet_data('Problems', 'A2:E')  # task_name 포함
    problems = []
    for row in values:
        if len(row) >= 4:
            problems.append({
                'set_number': row[0],    # A열 (문제집 번호)
                'task_name': row[1],     # B열 (문제 이름)
                'link': row[2],          # C열 (문제 링크)
                'description': row[3] if len(row) > 3 else "",  # D열 (문제 설명)
                'date_added': row[4] if len(row) > 4 else ""   # E열 (추가된 날짜)
            })
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