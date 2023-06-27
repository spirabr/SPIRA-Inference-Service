from core.model.inference import Inference, InferenceFiles
from core.model.result import ResultUpdate
import logging

logging.basicConfig(level = logging.INFO)

class ModelRegisterPort:
    """Port for the model register and model methods

    Args:
        message_service_adapter (Adapter Class) : model register adapter instance

    """

    def __init__(self, model_register_adapter):
        self._model_register_adapter = model_register_adapter

    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:
        """gets the model prediction on the inference

        Args:
            inference (Inference) : inference object
            inference_files (InferenceFiles) : files of the inference

        Returns:
            the result update object containing the prediction of the model

        """

        logging.info("Attempting to run predict on model register port")
        output, diagnosis = self._model_register_adapter.predict(
            inference, inference_files
        )
        logging.info("port output = ", output)
        logging.info("port diagnosis = ", diagnosis)

        return ResultUpdate(
            inference_id=inference.id, output=output, diagnosis=diagnosis
        )
