import mlflow
import os
import boto3
from typing import List, Tuple
from mlflow.pyfunc import PythonModel
import re

class ModelTemplate(PythonModel):

    def load_context(self, context) -> None:
      pass

    def predict(self, context, model_input) -> Tuple[List[float],str]:
      # model predict method should be implemented here
      pass

def register_model(model_name, model_topic_name):
  register_model_in_database(model_name, model_topic_name)
  register_model_in_mlflow()

def register_model_in_mlflow():
  print("registering model in mlflow...")
  mlflow.set_tracking_uri(os.environ["mlflow_conn_url"])
  model = ModelTemplate()

  boto3.connect_s3()
  s3 = boto3.client('s3')

  #minio is dumb and does not create buckets when they do not exist
  response = s3.create_bucket(
      Bucket=os.environ["MLFLOW_BUCKET_NAME"],
      CreateBucketConfiguration={
          'LocationConstraint': 'us-east-1'  # Specify the AWS region
      }
  )

  mlflow.pyfunc.log_model(
    artifact_path=os.environ["MLFLOW_BUCKET_NAME"],
    registered_model_name=model_name,
    python_model=model
  )

  print("model successfully registered in mlflow!")

def register_model_in_database(name, topic):
  print("registering model in database...")
  import requests
  import json
  token_response = requests.post(os.environ["AUTH_ENDPOINT"],data={"username": os.environ["SPIRA_API_USER"], "password": os.environ["SPIRA_API_PASSWORD"]})
  response_dict = json.loads(token_response.text)
  token = response_dict["access_token"]

  requests.post(os.environ["MODEL_CREATION_ENDPOINT"], headers={"Authorization": "Bearer " + token, "Content-Type": "application-json"}, data=json.dumps({"name": name, "publishing_channel": topic}))
  print("model successfully registered in database!")

if __name__=="__main__":
  model_name = os.environ["BOOTSTRAP_MODEL_NAME"]
  
  if not bool(re.match(r"[a-zA-Z0-9\-\_]+\Z",model_name)):
    print("Model name should be a string matching the regex [a-zA-Z0-9\-\_]+")
    raise SystemExit

  model_topic_name = model_name + "-topic"

  register_model(model_name,model_topic_name)