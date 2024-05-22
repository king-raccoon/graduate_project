import requests

# API 키와 Secret Key를 설정합니다.
client_id = ""  # 발급받은 Client ID를 입력하세요.
# 발급받은 Client Secret을 입력하세요.
client_secret = ""

# 분석하고 싶은 텍스트를 설정합니다.
texts = ["그는 사람을 열받게 하는데에 천부적인 재능을 타고 났다",
         "이틀이면 온다던 택배가 3주가 걸려 도착했다. 훌륭하다!", "와 아직도 덜했어? 대단하다"]
# Clova Sentiment API 엔드포인트와 헤더 정보
url = "https: // naveropenapi.apigw.ntruss.com/sentiment-analysis/"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json",
}

# 각 텍스트에 대해 반복하면서 감정 분석을 수행
for text in texts:
    data = {
        "content": text,
        # 부정적 세부 감정 분석 위해 config 옵션 추가
        "config": {
            "negativeClassification": True
        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        document_sentiment = result['document']['sentiment']  # 텍스트 감정 추출

        # 전체 감정 분석 결과 출력
        print(
            f"텍스트: {text}\n전체 감정 분석 결과: {document_sentiment}, 신뢰도: {result['document']['confidence']}\n")

        # 부정적인 감정 분석 결과 출력
        if document_sentiment == "negative":
            for sentence in result['sentences']:
                negative_sentiment = sentence.get('negativeSentiment', {})
                sentiment = negative_sentiment.get('sentiment', '정보 없음')
                confidence = negative_sentiment.get('confidence', 0)

                print(
                    f"문장: {sentence['content']}\n부정 감정: {sentiment}, 신뢰도: {confidence}\n")

    else:
        print(f"텍스트: {text}\n오류 발생: {response.status_code}\n")
