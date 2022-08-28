from src.adapters.model_register.mlflow_adapter import MLFlowAdapter
from src.adapters.model_register.model_base import ModelBase
from src.core.model.inference import Inference, InferenceFiles
from src.core.model.result import ResultUpdate


class ModelMock(ModelBase):
    def __init__(self):
        pass

    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:
        return [0.1, 0.2, 0.4], "negative"


class MLFlowMock(MLFlowAdapter):
    def __init__(self):
        self._model: ModelBase = ModelMock()
