from pathlib import Path
from typing import Any

from langchain.tools import StructuredTool

from src.context import Context
from src.models import CoverLetterData, CVData
from src.renderer import Renderer


class ToolProvider:
    """Supplementary class for tools usage by agent."""

    _renderer_implementation: Renderer
    _context: Context

    def __init__(self, renderer_implementation: Renderer, context: Context) -> None:
        """Init provider."""
        self._renderer_implementation = renderer_implementation
        self._context = context

    def render_cv(self, **kwargs: dict[str, Any]) -> Path:
        """Produce CV PDF from user input."""
        return self._renderer_implementation.render(
            CVData.model_validate(kwargs),
            self._context.output_path,
            "cv.html",
            "cv",
        )

    def render_cover_letter(self, **kwargs: dict[str, Any]) -> Path:
        """Produce cover letter PDF from user input."""
        return self._renderer_implementation.render(
            CoverLetterData.model_validate(kwargs),
            self._context.output_path,
            "cover_letter.html",
            "cover_letter",
        )

    @property
    def tools(self) -> dict[str, StructuredTool]:
        """Gives list of tools available to the agent."""
        return {
            "Render_CV": StructuredTool.from_function(  # pyright: ignore[reportUnknownMemberType]
                self.render_cv,
                name="Render_CV",
                description="Creates a CV with provided values",
                args_schema=CVData,
            ),
            "Render_cover_letter": StructuredTool.from_function(  # pyright: ignore[reportUnknownMemberType]
                self.render_cover_letter,
                name="Render_cover_letter",
                description="Creates a cover letter with provided values",
                args_schema=CoverLetterData,
            ),
        }
