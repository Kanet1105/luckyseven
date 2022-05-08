import requests

HOST = 'http://127.0.0.1:8000/{uri}'


class Payload:
    def __init__(self):
        self.placeInfo = {
            'placeName': "",
            'placeType': "",
            'placeAddress': "",
            'latitude': 0.0,
            'longitude': 0.0,
            'telephone': "",
            'description': "",
            'menu': dict(),
            'themeKeywords': [],
            'agePopularity': dict(),
            'genderPopularity': dict(),
            'time': dict(),
            'placeMeanRating': 0.0,
            'visitReviewNum': 0,
            'blogReviewNum': 0,
            'like': dict(),
        }

        self.reviewInfo = {
            'userHash': None,
            'reviewUserID': None,
            'placeName': None,
            'placeAddress': None,
            'reviewContent': None,
            'reviewInfoScore': None,
            'reviewInfoVisitDay': None,
            'reviewInfoVisitCount': 0,
        }

        self.userInfo = {
            'userHash': None,
            'userID': None,
            'reviewNum': 0,
            'photo': 0,
            'following': 0,
            'follower': 0,
        }

        self.placeNameInfo = {
            'placeName': None,
            'placeAddress': None
        }


def sendData(kind: str, data: dict):
    # requests.post 로 데이터 전송
    result = requests.post(url=HOST.format(uri=kind), json=data)
    print(result)

