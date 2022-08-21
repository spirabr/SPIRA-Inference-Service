from abc import ABC, abstractmethod

from core.model.result import ResultUpdate
from core.model.inference import Inference, InferenceFiles


class ModelBase(ABC):
    @abstractmethod
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
        pass
