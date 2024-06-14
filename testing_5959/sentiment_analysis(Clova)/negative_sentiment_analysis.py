import requests

# API 키와 Secret Key를 설정합니다.
client_id = "qssctpld4w"  # 발급받은 Client ID를 입력하세요.
# 발급받은 Client Secret을 입력하세요.
client_secret = ""

# 분석하고 싶은 텍스트를 설정합니다.
texts = ["아침에 일어나서 평소처럼 출근했고, 업무를 처리하면서 하루를 보냈다. 점심시간에는 동료들과 함께 식당에서 식사를 했다. 특별히 기억에 남는 일은 없었지만, 평화롭고 안정적인 하루였다. 저녁에는 집에서 책을 조금 읽고 일찍 잠자리에 들었다. 내일도 이렇게 평온한 하루가 되었으면 좋겠다.",
         "오늘은 정말 기분 좋은 하루였다. 오랜만에 친구들과 만나서 즐거운 시간을 보냈고, 맛있는 음식도 많이 먹었다. 오랜만에 웃음이 끊이지 않았다. 이런 소중한 순간들이 내 삶을 더 행복하게 만들어 준다는 것을 다시 한번 느꼈다. 오늘 같은 날이 더 많았으면 좋겠다.", "오늘은 정말 힘든 하루였다. 아침부터 일이 잘 풀리지 않아서 스트레스를 많이 받았다. 동료와의 불화로 인해 업무 분위기도 매우 어색했다. 집에 돌아와서도 마음이 무겁고, 아무것도 하고 싶지 않다. 내일이 조금이라도 나아지기를 바라면서 잠자리에 든다.", """오늘은 정말 복잡한 하루였다. 아침에 일어났을 때는 기분이 좋았다. 밖을 보니 날씨도 화창하고, 새들이 지저귀는 소리가 들려왔다. 그런데 회사에 도착하자마자 급한 프로젝트가 생겨서 온종일 바쁘게 일했다. 스트레스를 많이 받았고, 몸도 마음도 지쳐갔다. 하지만, 동료들이 도와줘서 어려움을 함께 극복할 수 있었다. 그 순간, 나는 직장에서의 우정과 동료애가 얼마나 소중한지 깨달았다.

점심시간에는 외롭고 슬픈 기분이 들었다. 혼자 식당에 앉아 있으니, 멀리 떨어져 사는 가족들이 많이 그리웠다. 그들과 함께 시간을 보내지 못하는 것이 아쉽고, 때로는 외로움을 느낀다. 하지만 점심을 먹고 난 후, 친구에게서 위로의 메시지를 받았다. 친구의 따뜻한 말 한마디가 마음을 크게 위로해 주었다.

오후에는 일이 조금 진정되어서, 잠시 쉬면서 창밖을 바라보았다. 해가 지는 모습이 너무 아름다워서, 잠시 모든 걱정을 잊고 감탄했다. 그 순간, 삶의 소중한 순간들을 더 자주 감사해야겠다고 다짐했다.

집에 돌아온 후에는 피곤함에 지쳐 바로 잠자리에 들었다. 하지만 오늘 하루 겪은 다양한 감정들이 마음속에서 뒤엉키며 잠을 설쳤다. 기쁨, 스트레스, 외로움, 감사함... 오늘 하루는 정말 복잡미묘한 감정의 롤러코스터였다. 그럼에도 불구하고, 이 모든 경험이 나를 더 강하고 성숙하게 만들어 준다는 것을 안다. 내일은 어떤 하루가 될지, 어떤 감정을 느낄지 궁금하다."""]

# Clova Sentiment API 엔드포인트와 헤더 정보
url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
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
