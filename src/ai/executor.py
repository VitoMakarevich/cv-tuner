from abc import ABC, abstractmethod

from src.ai.agent import cv_tuner_agent
from src.ai.tools import ToolProvider
from src.context import Context
from src.renderer import Renderer


class Executor(ABC):
    """Controls steps before and after agent execution."""

    @abstractmethod
    def execute(self, api_key: str, model: str, context: Context) -> None:
        """Start the flow."""


class AgenticExecutor(Executor):
    """Controls steps before and after agent execution."""

    def __init__(self, renderer: Renderer) -> None:
        """Set underlying implementation."""
        self._renderer = renderer

    def execute(self, api_key: str, model: str, context: Context) -> None:
        """Start the flow."""
        tools = ToolProvider(self._renderer, context)

        cv_tuner_agent(context, tools, api_key, model)
        context.save()
