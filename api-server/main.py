"""
The API server handle payload agnostic writes to the Nats Jetstream Server
"""

from fastapi import FastAPI
import pickle
from publisher import Publisher
from templates import schema

HOST = '{address}:{port}'
app = FastAPI()
pub = Publisher(HOST)


async def publish(data, subject, timeout, stream):
    payload = pickle.dumps(data.dict())
    ack = await pub.publish(subject, payload, timeout, stream)
    return ack


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: schema.PlaceInfoModel):
    return await publish(data, 'scraped', 2.0, 'data')


@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: schema.ReviewInfoModel):
    return await publish(data, 'scraped', 2.0, 'data')


@app.post('/UserInfoModel')
async def receiveUserInfo(data: schema.UserInfoModel):
    return await publish(data, 'scraped', 2.0, 'data')
