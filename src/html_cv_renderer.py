from pathlib import Path

import pikepdf
from weasyprint import HTML  # pyright: ignore[reportMissingTypeStubs]

from src.renderer import Renderable, Renderer


class HTMLCVRenderer(Renderer):
    """Produces a human readable output from structured input."""

    def __init__(self, template_path: Path) -> None:
        """Init."""
        super().__init__(template_path, True)

    def render(self, data: Renderable, output_path: Path, template: str, output_doc_name: str) -> Path:
        """Render given data into text."""
        output = self._env.get_template(template).render(**data.model_dump())
        with open(output_path / f"{output_doc_name}.html", "w") as f:
            f.write(output)
        output_path = output_path / f"{output_doc_name}.pdf"
        HTML(string=output).write_pdf(target=output_path)  # pyright: ignore[reportUnknownMemberType]
        with pikepdf.open(output_path, allow_overwriting_input=True) as pdf:
            pdf.open_metadata().clear()
            pdf.save(output_path)
        return output_path
