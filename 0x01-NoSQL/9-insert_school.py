#!/usr/bin/env python3
"""
Inserts into mongodb collection with pymongo
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ Insert into mongodb collection with pymongo """
    return mongo_collection.insert_one(kwargs).inserted_id
