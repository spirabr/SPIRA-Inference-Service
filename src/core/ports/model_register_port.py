from core.model.inference import Inference, InferenceFiles
from core.model.result import ResultUpdate


class ModelRegisterPort:
    def __init__(self, model_register_adapter):
        self._model_register_adapter = model_register_adapter

    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:

        output, diagnosis = self._model_register_adapter.predict(
            inference, inference_files
        )

        return ResultUpdate(
            inference_id=inference.id, output=output, diagnosis=diagnosis
        )
