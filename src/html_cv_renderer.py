from pathlib import Path

from jinja2 import Environment
from weasyprint import HTML  # pyright: ignore[reportMissingTypeStubs]

from src.cv_renderer import CVRenderer
from src.models import CVData


class HTMLCVRenderer(CVRenderer):
    """Produces a human readable output from structured input."""

    _template: str

    def __init__(self, template_path: Path) -> None:
        """Init."""
        with open(template_path) as f:
            self._template = f.read()

    def render(self, data: CVData, output_path: Path) -> Path:
        """Render given data into text."""
        env = Environment(
            loader=None,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        output = env.from_string(self._template).render(**data.model_dump())
        with open(output_path / "cv.html", "w") as f:
            f.write(output)
        output_path = output_path / "cv.pdf"
        HTML(string=output).write_pdf(target=output_path)  # pyright: ignore[reportUnknownMemberType]
        return output_path
