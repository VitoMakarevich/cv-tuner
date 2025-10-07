from dataclasses import dataclass
from pathlib import Path

root_dir_path = Path(__file__).parent.parent.resolve()
prompts_path = root_dir_path / "prompts"
prompt_template_path = root_dir_path / "template" / "prompt"
latex_template_path = root_dir_path / "template" / "latex"
html_template_path = root_dir_path / "template" / "html"
fake_cv = prompts_path / "test_experience.json"
fake_cover_letter = prompts_path / "test_cover_letter.json"


@dataclass
class Prompts:
    """Raw prompts input."""

    job_description: str
    system_prompt: str
    experience: str
    system_prompt_cover_letter: str
    task: str


def load_prompts(
    job_description_file: str = "job_description.md",
    system_prompt_file: str = "system_prompt.md",
    system_prompt_cover_letter_file: str = "system_prompt_cover_letter.md",
    experience_file: str = "experience.md",
    task_file: str = "task.md",
) -> Prompts:
    """Load prompts from local filesystem."""
    job_description_path = prompts_path / job_description_file
    system_prompt_path = prompts_path / system_prompt_file
    system_prompt_cover_letter_path = prompts_path / system_prompt_cover_letter_file
    experience_prompt_path = prompts_path / experience_file
    task_path = prompts_path / task_file
    if not job_description_path.exists():
        raise ValueError(f"{job_description_path.as_posix()} does not exist")
    if not system_prompt_path.exists():
        raise ValueError(f"{system_prompt_path.as_posix()} does not exist")
    if not experience_prompt_path.exists():
        raise ValueError(f"{experience_prompt_path.as_posix()} does not exist")
    with open(job_description_path, encoding="utf-8") as f:
        job_description = f.read()
    with open(system_prompt_path, encoding="utf-8") as f:
        system_prompt = f.read()
    with open(system_prompt_cover_letter_path, encoding="utf-8") as f:
        system_prompt_cover_letter = f.read()
    with open(experience_prompt_path, encoding="utf-8") as f:
        experience = f.read()
    with open(task_path, encoding="utf-8") as f:
        task = f.read()
    return Prompts(
        job_description=job_description,
        system_prompt=system_prompt,
        experience=experience,
        system_prompt_cover_letter=system_prompt_cover_letter,
        task=task,
    )
