"""
The API server handle payload agnostic writes to the Nats Jetstream Server
subscription must match the ORM class name.
"""

from fastapi import FastAPI
import pickle
from publisher import Publisher
import schema

HOST = '{address}:{port}'
app = FastAPI()
pub = Publisher(HOST.format(address='10.106.59.62', port='4222'))


async def publish(data, subject, timeout, stream, headers=None) -> object:
    payload = pickle.dumps(data.dict())
    ack = await pub.publish(subject, payload, timeout, stream, headers)
    return ack


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: schema.PlaceInfoModel) -> object:
    return await publish(data, 'placeInfo', 2.0, 'data')


@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: schema.ReviewInfoModel) -> object:
    return await publish(data, 'reviewInfo', 2.0, 'data')


@app.post('/UserInfoModel')
async def receiveUserInfo(data: schema.UserInfoModel) -> object:
    return await publish(data, 'userInfo', 2.0, 'data')
