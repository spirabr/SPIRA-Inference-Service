from src.adapters.model_repository.mlflow_adapter import MLFlowAdapter
from src.adapters.model_repository.model_base import ModelBase
from src.core.model.inference import Inference, InferenceFiles
from src.core.model.result import ResultUpdate


class ModelMock(ModelBase):
    def __init__(self):
        pass

    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:
        return ResultUpdate(
            inference_id="fake_inference_id",
            output=[0.1, 0.2, 0.4],
            diagnosis="negative",
        )


class MLFlowMock(MLFlowAdapter):
    def __init__(self):
        self._model: ModelBase = ModelMock()
