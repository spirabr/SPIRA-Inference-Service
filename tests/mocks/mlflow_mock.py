from typing import List, Tuple
from src.adapters.model_register.mlflow_adapter import MLFlowAdapter

class ModelMock():
    def __init__(self):
        pass

    def predict(
        self, model_input
    ) -> Tuple[List[float],str]:
        return [0.1, 0.2, 0.4], "negative"


class MLFlowMock(MLFlowAdapter):
    def __init__(self):
        self._model = ModelMock()
