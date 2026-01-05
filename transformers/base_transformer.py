"""Base transformer definition.

This module defines the abstract base class used by all transformers
in the transformation pipeline.
"""

from abc import ABC, abstractmethod
from typing import Any
from typing import Dict

class BaseTransformer(ABC):   
    """Define the interface for all transformers.

    All concrete transformers must implement the ``transform`` method,
    which takes a single dictionary item and returns a transformed
    dictionary.
    """

    @abstractmethod
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]: 
        """Transform a single dictionary item.

        Args:
            item: A dictionary representing a single configuration or
                URL entry.

        Returns:
            A transformed dictionary.
        """ 
        raise NotImplementedError
