def get_problems():
    """문제 목록 가져오기"""
    values = get_sheet_data('Problems', 'A2:D')
    problems = []
    for row in values:
        if len(row) >= 4:
            problems.append({
                'week': row[0],
                'links': row[1].split('\n'),
                'description': row[2],
                'date_added': row[3]
            })
    return problems

def save_submission(name, week, solution_link):
    """제출 정보 저장"""
    values = [
        name,
        week,
        solution_link,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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