from typing import List, Tuple
import mlflow as mlf
import mlflow.pytorch as pt

from adapters.model_register.model_base import ModelBase
from core.model.inference import Inference, InferenceFiles
from ...core.model.result import ResultUpdate


class MLFlowAdapter:
    def __init__(self, conn_url, model_path):
        mlf.set_tracking_uri(conn_url)
        self._model: ModelBase = pt.load_model(model_path)

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
        return self._model.predict(inference, inference_files)
