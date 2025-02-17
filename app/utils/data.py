import json
import pandas as pd
from .config import PROBLEMS_FILE, SUBMISSIONS_FILE

def load_problems():
    """문제 데이터 로드"""
    if PROBLEMS_FILE.exists():
        with open(PROBLEMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_submission(name, week, solution_link):
    """제출 데이터 저장"""
    submission = {
        "이름": name,
        "주차": week,
        "제출링크": solution_link,
        "제출시간": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if SUBMISSIONS_FILE.exists():
        df = pd.read_csv(SUBMISSIONS_FILE)
        df = pd.concat([df, pd.DataFrame([submission])], ignore_index=True)
    else:
        df = pd.DataFrame([submission])
    
    df.to_csv(SUBMISSIONS_FILE, index=False)