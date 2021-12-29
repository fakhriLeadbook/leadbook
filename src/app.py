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
    return "Leadbook Test 16"


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



    # file_name = request.json["file"]
    # year = file_name[-8:-4]






# =================================================================

    myclient = pymongo.MongoClient(env_.mongo_client)
    mydb = myclient["leadbook_db"]
    mycoll = mydb["tes1"]

    to_dict = df.to_dict("records")
    x = mycoll.insert_many(to_dict)

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
