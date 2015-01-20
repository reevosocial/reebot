#!/usr/bin/python
""" MongoDB connection module """

import pymongo
from config import db_params

class reemongo:
    def __init__(self):
        self.client = pymongo.MongoClient(db_params['uri'])
        self.db = self.client[db_params['database']]
        self.feed_list = self.db[db_params['feed_list']]
        self.log = self.db[db_params['log']]


