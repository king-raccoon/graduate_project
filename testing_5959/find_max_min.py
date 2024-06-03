# 파일에서 유사도 결과 읽기
similarities = {}
with open('testing_5959/semantic_similarity_results(Gemini).txt', 'r') as file:
    for line in file:
        parts = line.split(':')
        if len(parts) == 2:  # 올바른 형식의 줄인지 확인
            dialog_number = parts[0].strip()
            similarity = float(parts[1].strip()[:-1])
            similarities[dialog_number] = similarity

# 최대, 최소 유사도 및 해당 대화 찾기
max_similarity = max(similarities.values())
min_similarity = min(similarities.values())

max_dialog = [key for key, value in similarities.items() if value ==
              max_similarity][0]
min_dialog = [key for key, value in similarities.items() if value ==
              min_similarity][0]

# 결과 출력
print("최대 유사도:", max_similarity)
print("최대 유사도 대화:", max_dialog)
print("최소 유사도:", min_similarity)
print("최소 유사도 대화:", min_dialog)
