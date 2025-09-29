from pathlib import Path
from typing import Any

from langchain.tools import StructuredTool

from src.context import Context
from src.cv_renderer import CVRenderer
from src.models import CVData


class ToolProvider:
    """Supplementary class for tools usage by agent."""

    _renderer_implementation: CVRenderer
    _context: Context

    def __init__(self, renderer_implementation: CVRenderer, context: Context) -> None:
        """Init provider."""
        self._renderer_implementation = renderer_implementation
        self._context = context

    def render_cv(self, **kwargs: dict[str, Any]) -> Path:
        """Produce PDF from user input."""
        return self._renderer_implementation.render(CVData.model_validate(kwargs), self._context.output_path)

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
        }
