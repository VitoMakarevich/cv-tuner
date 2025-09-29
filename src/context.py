from pathlib import Path

from pydantic import BaseModel

from src.jinja_renderer import JinjaRenderer


class AgentInput(BaseModel):
    """Input used by Agent in runtime."""

    job_description: str
    experience: str
    system_prompt: str


class AllInput(BaseModel):
    """All input data used by Context."""

    raw_job_description: str
    raw_experience: str

    agent_input: AgentInput


class Context:
    """Runtime context used by agent to get and save values."""

    _all_input = AllInput
    _output_path: Path
    _tool_call: str | None = None

    def __init__(
        self,
        job_description: str,
        experience: str,
        system_prompt: str,
        output_path: Path,
        renderer: JinjaRenderer,
    ) -> None:
        """Render all input prompts and initialize internal structure."""
        output_path.mkdir(parents=True, exist_ok=True)
        self._output_path = output_path

        llm_job_description = renderer.render(
            "job_description.md.jinja",
            {"text": job_description},
        )
        llm_current_experience = renderer.render(
            "current_experience.md.jinja",
            {"text": experience},
        )
        agent_input = AgentInput(
            job_description=llm_job_description,
            experience=llm_current_experience,
            system_prompt=system_prompt,
        )
        self._all_input = AllInput(
            raw_job_description=job_description,
            raw_experience=experience,
            agent_input=agent_input,
        )

    @property
    def agent_input(self) -> AgentInput:
        """Give input to be used by agent."""
        return self._all_input.agent_input

    def save(self) -> None:
        """Save input known at this moment into output directory."""
        self._save_file(
            self._all_input.raw_job_description,
            self._output_path / "raw_job_description.md",
        )
        self._save_file(
            self._all_input.raw_experience,
            self._output_path / "raw_experience.md",
        )
        self._save_file(
            self._all_input.agent_input.job_description,
            self._output_path / "llm_job_description.md",
        )
        self._save_file(
            self._all_input.agent_input.experience,
            self._output_path / "llm_experience.md",
        )
        self._save_file(
            self._all_input.agent_input.system_prompt,
            self._output_path / "system_prompt.md",
        )
        if self._tool_call:
            self._save_file(self._tool_call, self._output_path / "tool_call.json")

    def _save_file(self, content: str, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def add_tool_call(self, tool_call: str) -> None:
        """Saves tool call result."""
        self._tool_call = tool_call

    @property
    def output_path(self) -> Path:
        """Output path for this context."""
        return self._output_path
