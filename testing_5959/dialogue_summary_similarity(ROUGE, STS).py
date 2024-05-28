import os
from sentence_transformers import SentenceTransformer, util
from rouge import Rouge
import numpy as np

# 파일을 읽어오는 함수


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Sentence-BERT를 사용하여 유사도를 계산하는 함수


def calculate_semantic_similarity(original_text, summary_text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode([original_text, summary_text])
    cosine_sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return cosine_sim.item() * 100

# ROUGE를 사용하여 유사도를 계산하는 함수


def calculate_rouge_similarity(original_text, summary_text):
    rouge = Rouge()
    scores = rouge.get_scores(summary_text, original_text, avg=True)
    rouge_1 = scores['rouge-1']['f'] * 100
    rouge_2 = scores['rouge-2']['f'] * 100
    rouge_l = scores['rouge-l']['f'] * 100
    return rouge_1, rouge_2, rouge_l


# 디렉토리 설정
base_directory = "testing_5959"
conversation_directory = os.path.join(base_directory, "dialogues")
summary_directory = os.path.join(base_directory, "summaries(OpenAI)")
results_filepath = os.path.join(
    base_directory, "semantic_similarity_results(ROUGE+STS).txt")

# 결과 파일 초기화
with open(results_filepath, 'w', encoding='utf-8') as results_file:
    results_file.write("Dialogue and Summary Semantic Similarity Results\n")
    results_file.write("=============================================\n\n")

# 전체 대화와 요약문의 유사도를 저장할 리스트
semantic_similarity_scores = []
rouge_1_scores = []
rouge_2_scores = []
rouge_l_scores = []

# 대화 파일과 요약 파일을 순회하며 유사도 계산
for idx in range(1, 301):  # 1부터 300까지
    dialogue_filename = f"{idx}th_dialog.txt"
    summary_filename = f"{idx}th_summary.txt"

    dialogue_filepath = os.path.join(conversation_directory, dialogue_filename)
    summary_filepath = os.path.join(summary_directory, summary_filename)

    # 디버깅을 위해 경로를 출력합니다.
    # print(f"Checking files: {dialogue_filepath} and {summary_filepath}")

    if os.path.exists(dialogue_filepath) and os.path.exists(summary_filepath):
        original_text = read_file(dialogue_filepath)
        summary_text = read_file(summary_filepath)

        semantic_similarity = calculate_semantic_similarity(
            original_text, summary_text)
        rouge_1, rouge_2, rouge_l = calculate_rouge_similarity(
            original_text, summary_text)

        semantic_similarity_scores.append(semantic_similarity)
        rouge_1_scores.append(rouge_1)
        rouge_2_scores.append(rouge_2)
        rouge_l_scores.append(rouge_l)

        result_line = (f"{idx}th dialog와 {idx}th summary의 유사도:\n"
                       f"Semantic 유사도: {semantic_similarity:.2f}%\n"
                       f"ROUGE-1: {rouge_1:.2f}%\n"
                       f"ROUGE-2: {rouge_2:.2f}%\n"
                       f"ROUGE-L: {rouge_l:.2f}%\n\n")
    else:
        result_line = f"{dialogue_filename} 또는 {
            summary_filename}이 존재하지 않습니다.\n"

    # 결과를 파일에 작성
    with open(results_filepath, 'a', encoding='utf-8') as results_file:
        results_file.write(result_line)

# 유사도 점수들의 평균 계산
average_semantic_similarity = np.mean(semantic_similarity_scores)
average_rouge_1 = np.mean(rouge_1_scores)
average_rouge_2 = np.mean(rouge_2_scores)
average_rouge_l = np.mean(rouge_l_scores)

# 평균을 결과 파일에 추가
with open(results_filepath, 'a', encoding='utf-8') as results_file:
    results_file.write(f"\n전체 대화와 요약문의 평균 유사도:\n"
                       f"Semantic 유사도: {average_semantic_similarity:.2f}%\n"
                       f"ROUGE-1: {average_rouge_1:.2f}%\n"
                       f"ROUGE-2: {average_rouge_2:.2f}%\n"
                       f"ROUGE-L: {average_rouge_l:.2f}%\n")

print(f"결과가 {results_filepath} 파일에 저장되었습니다.")
