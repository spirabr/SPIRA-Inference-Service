import logging
from typing import List, Tuple
import mlflow as mlf
import pandas as pd
from pandas import DataFrame
import os
import requests

from core.model.inference import Inference, InferenceFiles


class MLFlowAdapter:
    def __init__(self, conn_url, model_path):
        logging.info("setting mlflow adapter.")
        self._wait_for_server_connection()
        mlf.set_registry_uri(conn_url)
        logging.info("connected to mlflow server.")
        mlflow.pyfunc.get_model_dependencies(model_path)
        self._model = mlf.pyfunc.load_model(model_uri=model_path)
        logging.info("model loaded successfully.")
        
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
        return self._model.predict([inference.dict(),inference_files.dict()])

    def _wait_for_server_connection(self) -> None:
        os.system("sleep 5")
