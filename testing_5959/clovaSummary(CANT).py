!pip install requests

import zipfile
import os
import requests
import json
import re

# 아카이브 파일 경로 설정
archive_path = '/content/아카이브.zip'
extracted_path = '/content/extracted_files'
combined_text_path = '/content/combined_texts'

# 아카이브 파일 추출
with zipfile.ZipFile(archive_path, 'r') as archive:
    archive.extractall(extracted_path)

# Clova Summary API 설정
api_url = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
api_key_id = "secret"
api_key = "secret"

headers = {
    "Content-Type": "application/json",
    "X-NCP-APIGW-API-KEY-ID": api_key_id,
    "X-NCP-APIGW-API-KEY": api_key
}

def clean_text(text):
    # 텍스트 전처리: 불필요한 텍스트 제거 및 유효한 문장만 남기기
    text = re.sub(r'#@시스템#사진#', '', text)  # 시스템 메시지 제거
    text = re.sub(r'[^가-힣0-9\s]', '', text)  # 한글, 숫자, 공백 제외한 모든 문자 제거
    text = re.sub(r'\s+', ' ', text).strip()  # 여러 공백을 하나로 줄이기
    return text

def summarize_text(text):
    text = clean_text(text)  # 텍스트 전처리 적용
    if not text:
        print("Error: The text is empty or blank.")
        return None

    data = {
        "document": {
            "content": text
        },
        "option": {
            "language": "ko",
            "model": "general",
            "tone": 2,
            "summaryCount": 1
        }
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def process_files(input_path, combined_path, output_path):
    os.makedirs(combined_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    files = sorted([f for f in os.listdir(input_path) if f.endswith('.txt')])
    for i in range(0, len(files) - 1, 2):  # 두 개씩 처리
        file1 = files[i]
        file2 = files[i + 1]
        with open(os.path.join(input_path, file1), 'r', encoding='utf-8') as f1, \
             open(os.path.join(input_path, file2), 'r', encoding='utf-8') as f2:
            text1 = clean_text(f1.read())
            text2 = clean_text(f2.read())
            combined_text = text1 + " " + text2  # 텍스트를 공백으로 결합

            # 합친 텍스트 파일 저장
            combined_filename = f"{file1[:-4]}_{file2[:-4]}.txt"
            with open(os.path.join(combined_path, combined_filename), 'w', encoding='utf-8') as combined_file:
                combined_file.write(combined_text)

            # 요약 요청
            summary_response = summarize_text(combined_text)
            if summary_response and 'summary' in summary_response:
                summary = summary_response['summary']
                output_filename = f"{file1[:-4]}_{file2[:-4]}_summary.txt"
                with open(os.path.join(output_path, output_filename), 'w', encoding='utf-8') as out_file:
                    out_file.write(summary)
            else:
                print(f"Failed to summarize {file1} and {file2}")

# 파일 처리 경로
output_path = '/content/summaries'
process_files(extracted_path, combined_text_path, output_path)
