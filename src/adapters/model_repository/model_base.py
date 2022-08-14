from abc import ABC, abstractmethod

from core.model.result import ResultUpdate
from core.model.inference import Inference, InferenceFiles


class ModelBase(ABC):
    @abstractmethod
    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> ResultUpdate:
        pass
