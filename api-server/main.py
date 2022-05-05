from templates import schema
from fastapi import FastAPI


app = FastAPI()


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: schema.PlaceInfoModel):
    print(data)


@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: schema.ReviewInfoModel):
    print(data)


@app.post('/UserInfoModel')
async def receiveUserInfo(data: schema.UserInfoModel):
    print(data)
