from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

from jinja2 import Environment, FileSystemLoader

from src.models import CoverLetterData, CVData

Renderable = TypeVar("Renderable", CVData, CoverLetterData)


class Renderer(ABC):
    """Produces a human readable output from structured input."""

    _env: Environment

    def __init__(self, templates_path: Path, autoescape: bool) -> None:
        """Init."""
        self._env = Environment(
            loader=FileSystemLoader(templates_path),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=autoescape,  # noqa: S701 - Latex is used
        )

    @abstractmethod
    def render(self, data: Renderable, output_path: Path, template: str, output_doc_name: str) -> Path:
        """Render given data into text."""
