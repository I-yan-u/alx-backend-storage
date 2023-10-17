#!/usr/bin/env python3
"""
list of school
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    list of school having a specified topic
    """
    return mongo_collection.find({"topics": topic})
