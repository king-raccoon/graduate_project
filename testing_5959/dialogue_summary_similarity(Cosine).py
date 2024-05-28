import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

# 대화 내용 파일을 읽어오는 함수


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# BERT 모델을 사용하여 유사도를 계산하는 함수


def calculate_semantic_similarity(original_text, summary_text):
    """
    주어진 원문과 요약문 사이의 의미적 유사도를 계산합니다.

    :param original_text: 원문 (string)
    :param summary_text: 요약문 (string)
    :return: 두 문서 사이의 의미적 유사도 (percentage)
    """
    # 사전 훈련된 BERT 모델 로드
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # 문장 임베딩 생성
    embeddings = model.encode([original_text, summary_text])

    # 코사인 유사도 계산
    cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])

    # 유사도를 퍼센트로 변환하여 반환
    return cosine_sim.item() * 100


# 대화 내용이 있는 디렉토리
conversation_directory = "dialogues"
# 요약문이 저장된 디렉토리
summary_directory = "summaries"
# 결과를 저장할 파일
results_filepath = "semantic_similarity_results(Cosine).txt"

# 결과 파일 초기화
with open(results_filepath, 'w', encoding='utf-8') as results_file:
    results_file.write("Dialogue and Summary Semantic Similarity Results\n")
    results_file.write("=============================================\n\n")

# 전체 대화와 요약문의 유사도를 저장할 리스트
similarity_scores = []

# 대화 파일과 요약 파일을 순회하며 유사도 계산
for idx in range(1, 301):  # 1부터 300까지
    dialogue_filename = f"{idx}th_dialog.txt"
    summary_filename = f"{idx}th_summary.txt"

    dialogue_filepath = os.path.join(conversation_directory, dialogue_filename)
    summary_filepath = os.path.join(summary_directory, summary_filename)

    if os.path.exists(dialogue_filepath) and os.path.exists(summary_filepath):
        original_text = read_file(dialogue_filepath)
        summary_text = read_file(summary_filepath)

        similarity_percentage = calculate_semantic_similarity(
            original_text, summary_text)
        similarity_scores.append(similarity_percentage)
        result_line = f"{idx}th dialog와 {idx}th summary의 Semantic 유사도: {
            similarity_percentage:.2f}%\n"
    else:
        result_line = f"{dialogue_filename} 또는 {
            summary_filename}이 존재하지 않습니다.\n"

    # 결과를 파일에 작성
    with open(results_filepath, 'a', encoding='utf-8') as results_file:
        results_file.write(result_line)

# 유사도 점수들의 평균 계산
average_similarity = np.mean(similarity_scores)

# 평균을 결과 파일에 추가
with open(results_filepath, 'a', encoding='utf-8') as results_file:
    results_file.write(f"\n전체 대화와 요약문의 평균 Semantic 유사도: {
                       average_similarity:.2f}%\n")

print(f"결과가 {results_filepath} 파일에 저장되었습니다.")
