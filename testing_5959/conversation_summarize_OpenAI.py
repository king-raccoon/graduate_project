import os
from openai import OpenAI
import re

# OpenAI API 키 설정
client = OpenAI(
    api_key='',
)

# GPT를 사용하여 일기 생성하는 함수


def generate_diary(dialogue):
    messages = [
        {"role": "system", "content": "당신은 대화를 기반으로 P01이 작성한 일기를 자세하고 생각 깊게 작성하는 도우미입니다."},
        {"role": "user", "content": f"다음 대화를 바탕으로 P01이 작성한 일기를 작성해주세요. 대화에서 P01의 감정, 생각 및 중요한 사건을 잘 포함해 주세요.\n\n{dialogue}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

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
        summary_filepath = os.path.join(
            summary_directory, f"{idx}th_summary.txt")
        save_diary_to_file(generated_diary, summary_filepath)

print("작업이 완료되었습니다.")
