import json
import os

# dialogues 폴더가 없다면 생성
if not os.path.exists('dialogues'):
    os.makedirs('dialogues')

# sample.json 파일에서 데이터 읽기
with open('sample.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 대화문 순회
i = 1
for item in data['data']:
    # # 최대 100개의 대화문만 처리
    # if i >= 100:
    #     break

    if item['header']['dialogueInfo']['numberOfParticipants'] >= 3:
        continue
    # 참가자 수가 2인 경우에만 처리
    elif item['header']['dialogueInfo']['numberOfParticipants'] == 2:
        # 파일 이름 형식으로 저장 (e.g., 1th_dialog.txt)
        file_name = f"dialogues/{i}th_dialog.txt"
        i += 1

        # 파일에 대화문 저장
        with open(file_name, 'w', encoding='utf-8') as dialog_file:
            for utterance in item['body']['dialogue']:
                participant_id = utterance['participantID']
                utterance_text = utterance['utterance']
                # turnID : utterance 형태로 파일에 작성
                dialog_file.write(f"{participant_id}: {utterance_text}\n")
