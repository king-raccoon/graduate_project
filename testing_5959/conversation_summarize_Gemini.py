import os
import google.generativeai as genai
import re

API_KEY = "AIzaSyAFfmx2fwYhPryrTgRKGuzsMkHfR9Q8jjo"
genai.configure(api_key=API_KEY)

# Generative AI를 사용하여 일기 생성하는 함수
def generate_diary(dialogue):
    prompt = f"다음 대화의 전체 내용을 P01의 관점에서 일기 형식으로 요약해줘.\n\n{dialogue}"
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", safety_settings=safety_settings)
    response = model.generate_content(prompt)
    return response.text.strip()

# 대화 내용 파일을 읽어오는 함수
def read_conversation_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        conversation = file.read()
    return conversation

# 일기를 파일에 저장하는 함수
def save_diary_to_file(diary, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(diary)

# 파일 이름에서 숫자 부분만 추출하는 함수
def extract_numbers(filename):
    numbers = re.findall(r'\d+', filename)
    if numbers:
        return int(numbers[0])
    else:
        return float('inf')  # 숫자가 없는 경우 무한대로 설정하여 가장 큰 숫자로 처리

# 대화 내용이 있는 디렉토리
conversation_directory = "dialogues"
# 일기를 저장할 디렉토리
summary_directory = "summaries"

# 대화 내용 파일을 순회하며 일기 생성 및 저장
filenames = os.listdir(conversation_directory)
# 파일 이름을 숫자로 변환하여 정렬
sorted_filenames = sorted(filenames, key=extract_numbers)

for idx, filename in enumerate(sorted_filenames, 1):
    if filename.endswith(".txt") and idx <= 300:
        dialogue_filepath = os.path.join(conversation_directory, filename)
        print(dialogue_filepath)  # 파일 경로 출력
        dialogue = read_conversation_from_file(dialogue_filepath)
        generated_diary = generate_diary(dialogue)
        summary_filepath = os.path.join(summary_directory, f"{idx}th_summary.txt")
        save_diary_to_file(generated_diary, summary_filepath)

print("작업이 완료되었습니다.")