"""
Base Transformer Definition - Framework Layer.

This module defines the abstract base class (ABC) used by all transformers
within the generic transformation engine. It ensures a consistent interface
for reusable transformation components.
"""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict


class BaseTransformer(ABC):
    """
    Define the interface for all transformers.

    All concrete transformers must implement the ``transform`` method,
    which takes a single dictionary item and returns a transformed
    dictionary. This maintains a domain-agnostic execution model.
    """

    @abstractmethod
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single dictionary item.

        Args:
            item: A dictionary representing a single configuration or
                URL entry.

        Returns:
            A transformed dictionary.
        """
        raise NotImplementedError
