import logging

from flask import request
import pymongo
import numpy as np
import pandas as pd

from env import EnvironmentVar


class ProcessingData():

    def __init__(self, df):
        self.df = df
        self.year = request.json["file"][-8:-4]
        self.mongo = EnvironmentVar().mongo_client

    def getting_duckduckgo_api(self):

        df = self.df
        year = self.year

        env_ = EnvironmentVar()

        client = pymongo.MongoClient(env_.mongo_client)
        db = client["desc-url"]
        coll_api = db[year+" desc-url"]

        df["Description"] = np.nan
        df["URL"] = np.nan

        list_univ = df.iloc[:,1].values

        for i in range(len(list_univ)):
            try:
                result = coll_api.find_one({"query": list_univ[i]})
                desc = result["Abstract"]
                url = result["AbstractURL"]
            except Exception as e:
                logging.exception(e)
                desc = np.nan
                url = np.nan
            finally:         
                df.loc[i, "Description"] = desc
                df.loc[i, "URL"] = url

        self.enhance_data_from_api(df)

                

    def enhance_data_from_api(self, df):

        year = self.year
        mongo_key = self.mongo

        df["Year"] = year

        client = pymongo.MongoClient(mongo_key)
        db = client["leadbook_db"]
        coll_yearly = db["Yearly Ranking"]

        to_dict = df.to_dict("records")
        coll_yearly.insert_many(to_dict)

        coll_info = db["Universities Info"]
        coll_info.drop()

        to_dict = df.to_dict("records")
        coll_info.insert_many(to_dict)
