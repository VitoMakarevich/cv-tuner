import re
import subprocess
from pathlib import Path

from src.renderer import Renderable, Renderer


class LatexCVRenderer(Renderer):
    """Produces a human readable output from structured input."""

    def __init__(self, template_path: Path) -> None:
        """Init."""
        super().__init__(template_path, False)
        self._env.filters["le"] = self._escape_latex

    def render(self, data: Renderable, output_path: Path, template: str, output_doc_name: str) -> Path:
        """Render given data into text."""
        output = self._env.get_template(template).render(**data.model_dump())
        tex_path = output_path / f"{output_doc_name}.tex"
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(output)
        self._render_pdf_from_latex(tex_path)
        return output_path / f"{output_doc_name}.pdf"

    def _render_pdf_from_latex(self, tex_path: Path) -> None:
        """Given LaTex path - make a PDF from it."""
        tex_path_dir = tex_path.parent.resolve()
        cmds = [
            "pdflatex",
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            f"-output-directory={tex_path_dir.as_posix()}",
            tex_path.as_posix(),
        ]
        subprocess.run(cmds, check=True, capture_output=False)
        self._delete_files_with_extensions(tex_path_dir, ["aux", "log", "out", "gz"])

    def _delete_files_with_extensions(self, dir_path: Path, extensions: list[str]) -> None:
        """Delete all files in the given directory with specified extensions."""
        # Iterate over all extensions
        for ext in extensions:
            for file in dir_path.glob(f"*{ext}"):
                if file.is_file():
                    file.unlink()

    def _escape_latex(self, s: str) -> str:
        """Escape LaTeX special characters in a string, collapsing multiple newlines."""
        replacements = {
            "\\": r"\textbackslash{}",
            "{": r"\{",
            "}": r"\}",
            "$": r"\$",
            "&": r"\&",
            "#": r"\#",
            "_": r"\_",
            "%": r"\%",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "<": r"\textless{}",
            ">": r"\textgreater{}",
        }

        pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
        escaped = pattern.sub(lambda m: replacements[m.group()], s)

        escaped = re.sub(r"\n+", r"\\\[0.5em]", escaped)

        return escaped
