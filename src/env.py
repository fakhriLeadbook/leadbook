import os

class env_var(): 

    def __init__(self):
        self.aws_access_key_id = os.environ['aws_access_key_id'] 
        self.aws_secret_access_key = os.environ['aws_secret_access_key']
        self.mongo_client = os.environ['mongo_client']  
