from abc import ABC, abstractmethod
from typing import List, Tuple

from core.model.result import ResultUpdate
from core.model.inference import Inference, InferenceFiles


class ModelBase(ABC):
    @abstractmethod
    def predict(
        self, inference: Inference, inference_files: InferenceFiles
    ) -> Tuple[List[float], str]:
        """returns the model prediction for the given input

        Args:
            inference (Inference) : inference object containing inference metadata
            inference_files (InferenceFiles) : inference audio files object

        Returns:
            Tuple with list of outputs and diagnosis string

        """
        pass
