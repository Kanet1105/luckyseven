import requests

HOST = 'http://127.0.0.1:8000/{uri}'


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

    reviewInfo = {
        'userHash': None,
        'reviewUserID': None,
        'placeName': None,
        'placeAddress': None,
        'reviewContent': None,
        'reviewInfoScore': None,
        'reviewInfoVisitDay': None,
        'reviewInfoVisitCount': None,
    }

    userInfo = {
        'userHash': None,
        'userID': None,
        'reviewNum': None,
        'photo': None,
        'following': None,
        'follower': None,
    }

    placeNameInfo = {
        'placeName': None,
        'placeAddress': None
    }


def sendData(kind: str, data: dict):
    # requests.post 로 데이터 전송
    result = requests.post(url=HOST.format(uri=kind), json=data)
    print(result)
