from pymongo import MongoClient
from pymongo import errors
import traceback
import pymongo
import pickle


class MongoConnector:
    def __init__(
            self, dbName: str,
            errorLogger,
            dataLogger,
    ):
        self.client = MongoClient('127.0.0.1', 27017)
        self.collectionList = {'placeInfo': ('placeName', 'placeAddress'),
                               'reviewInfo': ('placeName', 'placeAddress', 'userHash', 'reviewInfoVisitCount'),
                               'userInfo': ('userHash'),
                               }
        self.db = self.makeDB(dbName)
        self.errorLogger = errorLogger
        self.dataLogger = dataLogger

    def makeDB(self, dbName):
        try:
            self.db = self.client[dbName]
            # make collection
            for cName, idxName in self.collectionList.items():
                self.db[cName]
                self.makeIndex(self.db[cName], idxName)
        except:
            raise Exception(traceback.format_exc())

    # 콜렉션마다 인덱스 만들기
    def makeIndex(self, collection, idxNames):
        try:
            if type(idxNames) == str:
                collection.create_index(idxNames, unique=True)
            else:
                collection.create_index([(idxEntry, pymongo.ASCENDING) for idxEntry in idxNames], unique=True)
        except:
            raise Exception(traceback.format_exc())

    def writeBatch(self, data, collection: str):
        data = pickle.loads(data)
        try:
            self.db[collection].insert_many(data)
        except errors.DuplicateKeyError:
            self.errorLogger.error("review 정보 이미 있습니다")
            self.dataLogger.error(data)
        except errors.BulkWriteError:
            self.errorLogger.error(traceback.format_exc())
            self.dataLogger.error(data)
        except:
            self.errorLogger.error(traceback.format_exc())
            self.dataLogger.error(data)