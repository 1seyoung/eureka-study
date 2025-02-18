from datetime import datetime
from .sheets import get_sheet_data, append_row

def get_problems():
    """Get problems data"""
    values = get_sheet_data('Problems', 'A2:D')
    problems = []
    for row in values:
        if len(row) >= 3:
            problems.append({
                'set_number': row[0],
                'link': row[1],
                'description': row[2] if len(row) > 2 else "",
                'date_added': row[3] if len(row) > 3 else ""
            })
    return problems

def save_submission(name, problem_set, problem_link, solution_link, group=''):
    """Save submission data"""
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
    values = get_sheet_data('Submissions', 'A2:D')
    submissions = []
    for row in values:
        if len(row) >= 4:
            submissions.append({
                '이름': row[0],
                '주차': row[1],
                '제출링크': row[2],
                '제출시간': row[3]
            })
    return submissions