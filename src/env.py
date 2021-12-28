import os

class EnvironmentVar(): 
    def __init__(self):
        self.aws_access_key_id = os.environ['aws_access_key_id'] 
        self.aws_secret_access_key = os.environ['aws_secret_access_key']
        self.mongo_client = os.environ['mongo_client']  


# class env_var(): #Camel Case

#     def __init__(self):
#         self.aws_access_key_id = os.environ['aws_access_key_id'] 
#         self.aws_secret_access_key = os.environ['aws_secret_access_key']
#         self.mongo_client = os.environ['mongo_client']  