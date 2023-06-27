import mlflow
import os
from minio import Minio
from typing import List, Tuple
from mlflow.pyfunc import PythonModel
import re

class ModelTemplate(PythonModel):

    def load_context(self, context) -> None:
      pass

    def predict(self, context, model_input) -> Tuple[List[float],str]:
      # model predict method should be implemented here
      return ([1.0, 2.0, 3.0, 4.0], "ajuda o maluco que ele ta doente")

def register_model(model_name, model_topic_name):
  register_model_in_database(model_name, model_topic_name)
  register_model_in_mlflow()

def register_model_in_mlflow():
  print("registering model in mlflow...")
  mlflow.set_tracking_uri(os.environ["mlflow_conn_url"])
  model = ModelTemplate()

  #minio is stupid and does not allow put objects in a bucket not yet created
  client = Minio(os.environ["minio_conn_url"], access_key=os.environ["minio_access_key"], 
                 secret_key=os.environ["minio_secret_key"], secure=False)

  bucket_name = os.environ["MLFLOW_BUCKET_NAME"]
  # Make 'asiatrip' bucket if not exist.
  found = client.bucket_exists(bucket_name)
  if not found:
      client.make_bucket(bucket_name)


  mlflow.pyfunc.log_model(
    artifact_path=bucket_name,
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

  requests.post(os.environ["MODEL_CREATION_ENDPOINT"], headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, data=json.dumps({"name": name, "publishing_channel": topic}))
  print("model successfully registered in database!")

if __name__=="__main__":
  model_name = os.environ["BOOTSTRAP_MODEL_NAME"]
  
  if not bool(re.match(r"[a-zA-Z0-9\-\_]+\Z",model_name)):
    print("Model name should be a string matching the regex [a-zA-Z0-9\-\_]+")
    raise SystemExit

  model_topic_name = model_name + "-topic"

  register_model(model_name,model_topic_name)