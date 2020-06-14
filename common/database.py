""" URI stands for Uniform Resource Identifier """
from typing import Dict
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    """ the database is named pricing in our case """

    URI = os.environ.get("MONGODB_URI")
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        """ The pymongo.cursor is a iterable """
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict):
        return Database.DATABASE[collection].remove(query)
