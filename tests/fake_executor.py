from src.ai.executor import Executor
from src.ai.tools import ToolProvider
from src.context import Context
from src.cv_renderer import CVRenderer
from src.models import CVData


class FakeExecutor(Executor):
    def __init__(self, renderer: CVRenderer) -> None:
        self._renderer = renderer

    def execute(self, api_key: str, model: str, context: Context) -> None:
        tool_provider = ToolProvider(self._renderer, context)
        context.save()

        cv_data = CVData.model_validate_json(context._all_input.raw_experience)  # pyright: ignore[reportPrivateUsage] - ok for tests
        tool_provider.tools["Render_CV"].invoke(cv_data.model_dump())  # pyright: ignore[reportUnknownMemberType]
