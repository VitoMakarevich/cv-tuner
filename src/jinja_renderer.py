from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class JinjaRenderer:
    """Render output files given template name and input data."""

    def __init__(self, template_path: Path) -> None:
        """Create Jinja primitives."""
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

    def render(self, template_name: str, data: dict[str, Any]) -> str:
        """Render Jinja template into str."""
        rendered = self.env.get_template(template_name).render(**data)
        return rendered
