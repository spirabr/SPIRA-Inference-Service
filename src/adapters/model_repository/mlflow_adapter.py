import mlflow as mlf
import mlflow.pytorch as pt

from adapters.model_repository.model_base import ModelBase
from core.model.inference import Inference, InferenceFiles


class MLFlowAdapter:
    def __init__(self, conn_url, model_path):
        mlf.set_tracking_uri(conn_url)
        self._model: ModelBase = pt.load_model(model_path)

    def predict(self, inference: Inference, inference_files: InferenceFiles):
        return self._model.predict(inference, inference_files)
