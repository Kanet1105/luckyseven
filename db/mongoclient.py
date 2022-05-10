from pymongo import MongoClient
from pymongo import errors
import traceback
import pymongo


class MongoConnector:
    def __init__(
            self,
            address: str,
            port: int,
            dbName: str,
            errorLogger,
            dataLogger,
    ):
        self.client = MongoClient(address, port)
        self.collectionList = {
            'placeInfo': ('placeName', 'placeAddress'),
            'reviewInfo': ('placeName', 'placeAddress', 'userHash', 'reviewInfoVisitCount'),
            'userInfo': ('userHash'),
        }
        self.db = None
        self.makeDB(dbName)
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

    def batchWrite(self, data: list, collectionName: str):
        try:
            print(self.db[collectionName].insert_many(data))
        except errors.DuplicateKeyError:
            self.errorLogger.logger.error('the review already exists.')
            self.dataLogger.logger.error(data)
        except errors.BulkWriteError:
            self.errorLogger.logger.error(traceback.format_exc())
            self.dataLogger.logger.error(data)
        except:
            self.errorLogger.logger.error(traceback.format_exc())
            self.dataLogger.logger.error(data)
