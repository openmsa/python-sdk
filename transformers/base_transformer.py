from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTransformer(ABC):
    """Abstract base class for all transformers."""

    @abstractmethod
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single dictionary item.
        Args:
            item: Input dictionary representing a URL entry.
        Returns:
            Transformed dictionary.
        """
        pass
