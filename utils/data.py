from .sheets import get_sheet_data

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