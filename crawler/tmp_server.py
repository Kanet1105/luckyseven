from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


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
    folloing: int
    follower: int


app = FastAPI()

@app.post('/data')
async def receiveData(data: PlaceInfoModel):
    print(data)

