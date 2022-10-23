from typing import List, Tuple
import mlflow as mlf
import pandas as pd
from pandas import DataFrame
import os
import requests

from core.model.inference import Inference, InferenceFiles


class MLFlowAdapter:
    def __init__(self, conn_url, model_path):
        print("setting mlflow adapter.", flush=True)
        self._wait_for_server_connection(conn_url)
        mlf.set_registry_uri(conn_url)
        print("connected to mlflow server.", flush=True)
        self._model = mlf.pyfunc.load_model(model_uri=model_path)
        
    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> Tuple[List[float], str]:   
        """returns the model prediction for the given input

        Args:
            inference (Inference) : inference object containing inference metadata
            inference_files (InferenceFiles) : inference audio files object

        Returns:
            Tuple where the first element is a list of floats containing the output of the model
            and the second element is the string containing the final diagnosis

        """
        return self._model.predict(self._build_dataframe(inference, inference_files))

    def _build_dataframe(inference: Inference, inference_files: InferenceFiles) -> DataFrame:
        inference_dataframe = pd.DataFrame.from_dict(inference.dict())

        inference_files_dataframe = pd.DataFrame.from_dict(inference_files.dict())

        return pd.concat(inference_dataframe,inference_files_dataframe)

    def _wait_for_server_connection(self, conn_url: str) -> None:
        os.system("sleep 10")