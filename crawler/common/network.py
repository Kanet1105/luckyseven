import traceback

import requests

HOST = 'http://61.254.240.172:30000/{uri}'


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


def sendData(kind: str, data: dict, errorLogger):
    try:
        # requests.post 로 데이터 전송
        result = requests.post(url=HOST.format(uri=kind), json=data)
        print(result)
        if result.status_code == 200:
            return True
        else:
            return False
    except:
        print(traceback.format_exc())
        errorLogger.logger.error(data)
