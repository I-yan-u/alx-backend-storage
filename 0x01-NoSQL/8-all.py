#!/usr/bin/python3
"""
pymongo
"""
import pymongo

def list_all(mongo_collection):
    """ Reurn all documents in the collection """
    if not mongo_collection.find():
        return []
    return list(mongo_collection.find())
