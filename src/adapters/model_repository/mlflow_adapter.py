import mlflow as mlf
import mlflow.pytorch as pt

from adapters.model_repository.model_base import ModelBase
from core.model.inference import Inference, InferenceFiles
from ...core.model.result import ResultUpdate


class MLFlowAdapter:
    def __init__(self, conn_url, model_path):
        mlf.set_tracking_uri(conn_url)
        self._model: ModelBase = pt.load_model(model_path)

    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:
        """returns the model prediction for the given input

        Args:
            inference (Inference) : inference object containing inference metadata
            inference_files (InferenceFiles) : inference audio files object

        Returns:
            ResultUpdate object containing the model prediction

        """
        return self._model.predict(inference, inference_files)
