import os
from datetime import datetime

from src.ai.executor import AgenticExecutor
from src.context import Context
from src.html_cv_renderer import HTMLCVRenderer
from src.jinja_renderer import JinjaRenderer
from src.local_file_loader import html_template_path, load_prompts, prompt_template_path, root_dir_path

expected_files = [
    "cv.pdf",
    "cv.html",
    "cover_letter.pdf",
    "cover_letter.html",
    "llm_experience.md",
    "llm_job_description.md",
    "raw_experience.md",
    "raw_job_description.md",
    "system_prompt.md",
    "cover_letter.pdf",
    "system_prompt_cover_letter.md",
]

jinja_renderer = JinjaRenderer(prompt_template_path)
html_renderer = HTMLCVRenderer(html_template_path)


# @pytest.mark.skip
def test_real() -> None:
    output_path = root_dir_path / "test_output" / datetime.now().isoformat()
    api_key = os.environ["OPENAI_API_KEY"]
    assert api_key is not None
    prompts = load_prompts()
    context = Context(
        job_description=prompts.job_description,
        experience=prompts.experience,
        system_prompt=prompts.system_prompt,
        system_prompt_cover_letter=prompts.system_prompt_cover_letter,
        task=prompts.task,
        output_path=output_path,
        renderer=jinja_renderer,
    )
    executor = AgenticExecutor(html_renderer)
    executor.execute(api_key, "gpt-5-nano", context)
    output_files = os.listdir(output_path)
    assert set(expected_files + ["tool_call.json"]).issuperset(set(output_files))
