from fastapi import FastAPI
from pymongo import MongoClient
import pymongo
import schema



app = FastAPI()


# 콜렉션마다 인덱스 만들기
def makeIdx(collection, idxnames):
    try:
        if type(idxnames) == str:
            collection.create_index(idxnames, unique=True)
        else:
            collection.create_index([(idxname, pymongo.ASCENDING) for idxname in idxnames], unique=True)
    except:
        print("Index already exist")


# DB생성
def makeDB(dbname, collection):
    try:
        client = MongoClient('127.0.0.1', 27017)
        db = client[dbname]
        # make collection
        for cname, idxname in collection.items():
            globals()[cname] = db[cname]
            makeIdx(globals()[cname], idxname)
    except:
        print("DB already exist")

    return db


# 디버깅 프린트
def debugPrint(data, mode='first'):
    if mode == 'first':
        print("처음 데이터(타입): ", type(data))
        print("처음 데이터(데이터): ", data)
    if mode == 'insert':
        print("삽입 후(타입): ", type(data))
        print("삽입 후(데이터): ", data)
    if mode == 'exist':
        print("이미 있음(타입): ", type(data))
        print("이미 있음(데이터): ", data)


# DB저장 위한 INFO(key = Collection명, value = Index명)
collectionList = {'placeInfo': ('placeName', 'placeAddress'),
                  'reviewInfo': ('placeName', 'placeAddress', 'userHash', 'reviewInfoVisitCount'),
                  'userInfo': ('userHash')}
# DB생성
db = makeDB('test2', collectionList)


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: schema.PlaceInfoModel):
    print("*" *20 , "장소정보 저장", "*"*20)
    data = dict(data)
    debugPrint(data, mode='first')

    try:
        result = db['placeInfo'].insert_one(data)
        debugPrint(result, mode='insert')

    except:
        print("place 정보 이미 있습니다")
        alreadyData = db['placeInfo'].find_one({'placeName': data['placeName'], 'placeAddress': data['placeAddress']})
        debugPrint(alreadyData, mode='exist')


@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: schema.ReviewInfoModel):
    data = dict(data)
    debugPrint(data, mode='first')
    try:
        print("*" * 20, "리뷰정보 저장", "*" * 20)
        result = db['reviewInfo'].insert_one(data)
        debugPrint(result, mode='insert')
    except:
        print("review 정보 이미 있습니다")
        alreadyData = db['reviewInfo'].find(
            {'placeName': data['placeName'],
             'placeAddress': data['placeAddress'],
             'userHash': data['userHash'],
             'reviewInfoVisitCount': data['reviewInfoVisitCount']
             }
        )
        debugPrint(alreadyData, mode='exist')


@app.post('/UserInfoModel')
async def receiveUserInfo(data: schema.UserInfoModel):
    print("*" * 20, "유저정보 저장", "*" * 20)
    data = dict(data)
    debugPrint(data, mode='first')

    try:
        result = db['userInfo'].insert_one(data)
        debugPrint(result, mode='insert')

    except:
        print("user 정보 이미 있습니다")
        alreadyData = db['userInfo'].find_one({'userHash': data['userHash']})
        debugPrint(alreadyData, mode='exist')

