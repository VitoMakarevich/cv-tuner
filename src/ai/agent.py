from typing import TYPE_CHECKING, cast

from langchain.schema import HumanMessage, SystemMessage
from pydantic import SecretStr

if TYPE_CHECKING:
    from langchain_core.messages import AIMessage

from langchain_openai import ChatOpenAI

from src.ai.tools import ToolProvider
from src.context import Context


def cv_tuner_agent(context: Context, tool_provider: ToolProvider, openai_api_key: str, open_api_model: str) -> None:
    """Agent that produces high-match CV.

    Agent that accepts candidate previous experience, job requirements and CV requirements and produces a high-match
    ratio CV.
    """
    llm = ChatOpenAI(
        model=open_api_model,
        output_version="responses/v1",
        verbose=True,
        api_key=SecretStr(openai_api_key),
    )
    tools = tool_provider.tools

    llm_with_tools = llm.bind_tools(list(tools.values()))  # pyright: ignore[reportUnknownMemberType]
    llm_input = context.agent_input
    system_prompt_cv = SystemMessage(content=llm_input.system_prompt)
    system_prompt_cover_letter = SystemMessage(content=llm_input.system_prompt_cover_letter)
    experience_message = HumanMessage(content=llm_input.experience)
    job_description_message = HumanMessage(content=llm_input.job_description)
    task = HumanMessage(llm_input.task)
    response = llm_with_tools.invoke(
        [
            system_prompt_cv,
            system_prompt_cover_letter,
            experience_message,
            job_description_message,
            task,
        ],
    )
    response = cast("AIMessage", response)

    if len(response.tool_calls) == 0:
        raise ValueError("Tool call number is 0, a tool must be called.")
    for tool_call in response.tool_calls:
        tools[tool_call["name"]].invoke(tool_call["args"])  # pyright: ignore[reportUnknownMemberType]
    import json

    context.add_tool_call(json.dumps(response.tool_calls))
    context.add_tool_call(json.dumps(response.tool_calls))
