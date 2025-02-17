import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheets_service():
    """Google Sheets API 서비스 객체 생성"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def get_sheet_data(sheet_name, range_name):
    """시트 데이터 읽기"""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=st.secrets["sheets"]["spreadsheet_id"],
        range=f'{sheet_name}!{range_name}'
    ).execute()
    
    return result.get('values', [])

def append_row(sheet_name, values):
    """시트에 새 행 추가"""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    body = {
        'values': [values]
    }
    
    result = sheet.values().append(
        spreadsheetId=st.secrets["sheets"]["spreadsheet_id"],
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    return result