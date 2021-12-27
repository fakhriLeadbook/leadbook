from flask import Flask, jsonify, request
import pandas as pd
import pymongo
import boto3

from env import env_var


app = Flask(__name__)


@app.route('/')
def index():
    return "Leadbook Test 5"


@app.route('/insert', methods=['POST'])
def inst():

    env_ = env_var()

    s3 = boto3.resource('s3',
                        aws_access_key_id=env_.aws_access_key_id,
                        aws_secret_access_key=env_.aws_secret_access_key
    )

    obj = s3.meta.client.get_object(Bucket= request.json["bucket"], Key= request.json["file"]) 
    df = pd.read_csv(obj['Body'], sep="\t")
     

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


