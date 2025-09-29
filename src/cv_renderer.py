from abc import ABC, abstractmethod
from pathlib import Path

from src.models import CVData


class CVRenderer(ABC):
    """Produces a human readable output from structured input."""

    @abstractmethod
    def render(self, data: CVData, _output_path: Path) -> Path:
        """Render given data into text."""
