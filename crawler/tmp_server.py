from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import pymongo


class PlaceInfoModel(BaseModel):
    placeName: str
    placeType: str
    placeAddress: str
    latitude: Optional[float]
    longitude: Optional[float]
    telephone: Optional[str]
    description: Optional[str]
    menu: Optional[dict]
    themeKeywords: Optional[list]
    agePopularity: Optional[dict]
    genderPopularity: Optional[dict]
    time: Optional[dict]
    placeMeanRating: Optional[float]
    visitReviewNum: Optional[int]
    blogReviewNum: Optional[int]
    like: Optional[dict]


class ReviewInfoModel(BaseModel):
    userHash: str
    reviewUserID: str
    placeName: str
    placeAddress: str
    reviewContent: Optional[str]
    reviewInfoScore: Optional[str]
    reviewInfoVisitDay: Optional[str]
    reviewInfoVisitCount: Optional[int]


class UserInfoModel(BaseModel):
    userHash: str
    userID: str
    reviewNum: int
    photo: int
    following: int
    follower: int


app = FastAPI()

placeMultiline = []
reviewMultiline = []
userMultiline = []
BATCH_SIZE = 20

client = MongoClient('127.0.0.1', 27017)

db = client['test']

# create collection
placeInfo = db['placeInfo']
reviewInfo = db['reviewInfo']
userInfo = db['userInfo']

# create unique index
placeInfo.create_index([('placeName', pymongo.ASCENDING), ('placeAddress', pymongo.ASCENDING)], unique=True)
reviewInfo.create_index(
    [
        ('placeName', pymongo.ASCENDING), ('placeAddress', pymongo.ASCENDING),
        ('userHash', pymongo.ASCENDING), ('reviewInfoVisitCount', pymongo.ASCENDING)
     ], unique=True)
userInfo.create_index('userHash', unique=True)


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: PlaceInfoModel):
    #placeMultiline.append(data)

    data = dict(data)

    print("처음 데이터(타입): ", type(data))
    print("처음 데이터(데이터): ", data)

    #if len(placeMultiline) == BATCH_SIZE:
    try:
        result = placeInfo.insert_one(data)
        print("삽입 후(타입): ", type(result))
        print("삽입 후(데이터): ", result)
    except:
        print("place 정보 이미 있습니다")
        alreadyData = placeInfo.find_one({'placeName': data['placeName'], 'placeAddress': data['placeAddress']})
        print("이미 있음(타입): ", type(alreadyData))
        print("이미 있음(데이터): ", alreadyData)
    # placeMultiline.clear()


@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: ReviewInfoModel):
    #reviewMultiline.append(data)

    data = dict(data)

    print("처음 데이터(타입): ", type(data))
    print("처음 데이터(데이터): ", data)

    #if len(reviewMultiline) == BATCH_SIZE:
    try:
        result = reviewInfo.insert_one(data)
        print("삽입 후(타입): ", type(result))
        print("삽입 후(데이터): ", result)
    except:
        print("review 정보 이미 있습니다")
        alreadyData = placeInfo.find_one(
            {'placeName': data['placeName'],
             'placeAddress': data['placeAddress'],
             'userHash': data['userHash'],
             'reviewInfoVisitCount': data['reviewInfoVisitCount']
             }
        )
        print("이미 있음(타입): ", type(alreadyData))
        print("이미 있음(데이터): ", alreadyData)
    # reviewMultiline.clear()

    #return result

@app.post('/UserInfoModel')
async def receiveUserInfo(data: UserInfoModel):
    #userMultiline.append(data)

    data = dict(data)

    print("처음 데이터(타입): ", type(data))
    print("처음 데이터(데이터): ", data)

    #if len(userMultiline) == BATCH_SIZE:
    try:
        result = userInfo.insert_one(data)
        print("삽입 후(타입): ", type(result))
        print("삽입 후(데이터): ", result)
    except:
        print("user 정보 이미 있습니다")
        alreadyData = placeInfo.find_one({'userHash': data['userHash']})
        print("이미 있음(타입): ", type(alreadyData))
        print("이미 있음(데이터): ", alreadyData)
    # userMultiline.clear()