import requests

HOST = 'http://127.0.0.1:8000/data'

class Payload:
    placeInfo = {
        'placeName': None ,
        'placeType': None,
        'placeAddress': None,
        'latitude': None,
        'longitude': None,
        'telephone': None,
        'description': None,
        'menu': dict(),
        'themeKeywords': [],
        'agePopularity': dict(),
        'genderPopularity': dict(),
        'time': dict(),
        'placeMeanRating': None,
        'visitReviewNum': None,
        'blogReviewNum': None,
        'like': dict(),
    }

def sendData(kind: str, data: dict):
    # requests.post 로 데이터 전송
    if kind == "placeInfo":
        result = requests.post(url=HOST, json=data)
        print(result)
    pass
