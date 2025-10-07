from openai import BaseModel

from src.ai.executor import Executor
from src.ai.tools import ToolProvider
from src.context import Context
from src.local_file_loader import fake_cover_letter, fake_cv
from src.models import CoverLetterData, CVData
from src.renderer import Renderer


class FakeData(BaseModel):
    cv: CVData
    cover_letter: CoverLetterData


class FakeExecutor(Executor):
    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer
        self._fake_data = FakeData(
            cv=CVData.model_validate_json(open(fake_cv).read()),
            cover_letter=CoverLetterData.model_validate_json(open(fake_cover_letter).read()),
        )

    def execute(self, api_key: str, model: str, context: Context) -> None:
        tool_provider = ToolProvider(self._renderer, context)
        context.save()

        tool_provider.tools["Render_CV"].invoke(self._fake_data.cv.model_dump())  # pyright: ignore[reportUnknownMemberType]
        tool_provider.tools["Render_cover_letter"].invoke(self._fake_data.cover_letter.model_dump())  # pyright: ignore[reportUnknownMemberType]
