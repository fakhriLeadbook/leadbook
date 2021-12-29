import time
import logging
import random

from flask import Flask, jsonify, request
import pandas as pd
import pymongo
import boto3
import requests
import numpy as np

from env import EnvironmentVar


app = Flask(__name__)


@app.route('/')
def index():
    return "Leadbook Test 19"


@app.route('/insert', methods=['POST'])
def inst():

    env_ = EnvironmentVar()

    s3 = boto3.resource('s3',
                        aws_access_key_id=env_.aws_access_key_id,
                        aws_secret_access_key=env_.aws_secret_access_key
    )

    obj = s3.meta.client.get_object(Bucket= request.json["bucket"], Key= request.json["file"]) 
    df = pd.read_csv(obj['Body'], sep="\t")
     

# =================================================================


    file_name = request.json["file"]
    year = file_name[-8:-4]


    def cleaning_function(input_):   
        if type(input_) == float or type(input_) == int:
            output = input_
        elif input_.strip() == '-':
            output = np.nan
        else:
            output = input_
        return output

    def cleaning_more_than(input_):
        if type(input_) == float or type(input_) == int:
            output = input_
        elif input_.strip() == "> 1000":
            output = np.nan
        else:
            output = input_
        return output    

    for i in range(len(df.columns)):
        df.iloc[:,i] = df.iloc[:,i].apply(cleaning_function)
        df.iloc[:,i] = df.iloc[:,i].apply(cleaning_more_than)



    list_univ = df.iloc[:,1].values

    client = pymongo.MongoClient("mongodb+srv://fakhri:leadbookmongopassword123@cluster0.bnnky.mongodb.net/leadbook_db?retryWrites=true&w=majority")
    db = client["desc-url"]
    coll_api = db[year+" desc-url"]

    df["Description"] = np.nan
    df["URL"] = np.nan

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
            



    df["Year"] = year

    client = pymongo.MongoClient("mongodb+srv://fakhri:leadbookmongopassword123@cluster0.bnnky.mongodb.net/leadbook_db?retryWrites=true&w=majority")
    db = client["leadbook_db"]
    coll_yearly = db["Yearly Ranking"]

    to_dict = df.to_dict("records")
    coll_yearly.insert_many(to_dict)

    coll_info = db["Universities Info"]
    coll_info.drop()

    to_dict = df.to_dict("records")
    coll_info.insert_many(to_dict)



# =================================================================

    # myclient = pymongo.MongoClient(env_.mongo_client)
    # mydb = myclient["leadbook_db"]
    # mycoll = mydb["tes1"]

    # to_dict = df.to_dict("records")
    # x = mycoll.insert_many(to_dict)

    return jsonify({'result' : "success"})


@app.route('/test')
def test():
    return "Works!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





# def inst():
    
#     env_ = EnvironmentVar()

#     s3 = boto3.resource('s3',
#                         aws_access_key_id=env_.aws_access_key_id,
#                         aws_secret_access_key=env_.aws_secret_access_key
#     )

#     obj = s3.meta.client.get_object(Bucket= request.json["bucket"], Key= request.json["file"]) 
#     df = pd.read_csv(obj['Body'], sep="\t")
     

#     myclient = pymongo.MongoClient(env_.mongo_client)
#     mydb = myclient["leadbook_db"]
#     mycoll = mydb["tes1"]

#     to_dict = df.to_dict("records")
#     x = mycoll.insert_many(to_dict)

#     return jsonify({'result' : "success"})
