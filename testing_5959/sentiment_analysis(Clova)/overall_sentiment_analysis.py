import requests


# 전반적인 내용 분석 결과
# 분석하고 싶은 텍스트를 설정합니다.
texts = ["아침에 일어나서 평소처럼 출근했고, 업무를 처리하면서 하루를 보냈다. 점심시간에는 동료들과 함께 식당에서 식사를 했다. 특별히 기억에 남는 일은 없었지만, 평화롭고 안정적인 하루였다. 저녁에는 집에서 책을 조금 읽고 일찍 잠자리에 들었다. 내일도 이렇게 평온한 하루가 되었으면 좋겠다.",
         "오늘은 정말 기분 좋은 하루였다. 오랜만에 친구들과 만나서 즐거운 시간을 보냈고, 맛있는 음식도 많이 먹었다. 오랜만에 웃음이 끊이지 않았다. 이런 소중한 순간들이 내 삶을 더 행복하게 만들어 준다는 것을 다시 한번 느꼈다. 오늘 같은 날이 더 많았으면 좋겠다.", "오늘은 정말 힘든 하루였다. 아침부터 일이 잘 풀리지 않아서 스트레스를 많이 받았다. 동료와의 불화로 인해 업무 분위기도 매우 어색했다. 집에 돌아와서도 마음이 무겁고, 아무것도 하고 싶지 않다. 내일이 조금이라도 나아지기를 바라면서 잠자리에 든다."]

# Clova Sentiment API 엔드포인트와 헤더 정보
url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json",
}

# 각 텍스트에 대해 반복하면서 감정 분석을 수행
for text in texts:
    data = {"content": text}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        print(f"텍스트: {text}\n감정 분석 결과: {result}\n")
    else:
        print(f"텍스트: {text}\n오류 발생: {response.status_code}\n")
