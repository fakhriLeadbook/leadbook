from flask import Flask, jsonify, request
import pandas as pd
import boto3

from env import EnvironmentVar
from cleaning import CleaningData
from processing import ProcessingData


app = Flask(__name__)


@app.route('/')
def index():
    return "Leadbook Test"


@app.route('/insert', methods=['POST'])
def inst():

    env_ = EnvironmentVar()

    s3 = boto3.resource('s3',
                        aws_access_key_id=env_.aws_access_key_id,
                        aws_secret_access_key=env_.aws_secret_access_key)

    obj = s3.meta.client.get_object(Bucket= request.json["bucket"], Key= request.json["file"]) 
    df = pd.read_csv(obj['Body'], sep="\t")
     

    clean = CleaningData()

    for i in range(len(df.columns)):
        df.iloc[:,i] = df.iloc[:,i].apply(clean.cleaning_function)
        df.iloc[:,i] = df.iloc[:,i].apply(clean.cleaning_more_than)

    process = ProcessingData(df)
    process.getting_duckduckgo_api()


    return jsonify({'result' : "success"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')






