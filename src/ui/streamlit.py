import datetime
import os
from pathlib import Path

import streamlit as st

from src.ai.executor import AgenticExecutor
from src.context import Context
from src.html_cv_renderer import HTMLCVRenderer
from src.jinja_renderer import JinjaRenderer
from src.local_file_loader import html_template_path, load_prompts, prompt_template_path, root_dir_path
from tests.fake_executor import FakeExecutor

if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]

if "processing" not in st.session_state:
    st.session_state.processing = False
if "last_output" not in st.session_state:
    st.session_state.last_output = None

default_prompts = load_prompts()


def flow() -> None:
    """Main CV generation flow."""
    output_path = root_dir_path / "streamlit_output" / datetime.datetime.now().isoformat()
    renderer = JinjaRenderer(prompt_template_path)
    cv_renderer = HTMLCVRenderer(html_template_path)
    if preview:
        structured_defaults = load_prompts(experience_file="test_experience.json")
        context = Context(
            renderer=renderer,
            output_path=output_path,
            job_description=structured_defaults.job_description,
            experience=structured_defaults.experience,
            system_prompt=structured_defaults.system_prompt,
        )

        fake_executor = FakeExecutor(cv_renderer)
        fake_executor.execute("", "", context)
    else:
        context = Context(
            renderer=renderer,
            output_path=output_path,
            job_description=job_description,
            experience=experience,
            system_prompt=system_prompt,
        )

        real_executor = AgenticExecutor(cv_renderer)
        real_executor.execute(api_key, model, context)
    st.session_state.last_output = output_path / "cv.pdf"
    st.session_state.processing = False
    st.rerun()


@st.cache_data
def load_tool_description() -> str:
    """Loads tool description."""
    with open(Path(__file__).parent.parent.parent.resolve() / "tool_description.md", encoding="utf-8") as f:
        tool_description_markdown = f.read()
    return tool_description_markdown


st.set_page_config(
    page_title="CV Tuner",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.expander("📄 How to use AI CV Tuner", expanded=False):
    st.markdown(load_tool_description())

st.sidebar.header("📄 CV Inputs")

preview = st.sidebar.checkbox("👀 Preview", False, help="Do not use GPT - just render PDF with default values.")
if not preview:
    model = st.sidebar.selectbox(
        "🤖 Model",
        ["gpt-5-nano", "gpt-5-mini", "gpt-5", "gpt-4-o"],
        index=1,
        help="Select a model or type a custom one.",
        accept_new_options=True,
    )
    api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")

    TEXTAREA_HEIGHT = 150
    system_prompt = st.sidebar.text_area(
        "🛠️ System Prompt",
        default_prompts.system_prompt,
        height=TEXTAREA_HEIGHT,
        help="All instructions on how to merge your experience with desired job.",
    )
    job_description = st.sidebar.text_area(
        "💼 Job Description",
        default_prompts.job_description,
        height=TEXTAREA_HEIGHT,
        help="Copy-paste the entire job description here.",
    )
    experience = st.sidebar.text_area(
        "📝 Experience",
        default_prompts.experience,
        height=TEXTAREA_HEIGHT,
        help="Put your current version of resume - include all things you worked with, "
        "including simple ones like Git, Linux, etc.",
    )

submit = st.sidebar.button(
    "🚀 Make my resume",
    disabled=st.session_state.processing,
)

if submit:
    st.session_state.last_output = None
    st.session_state.processing = True
if st.session_state.last_output is None and st.session_state.processing:
    with st.spinner("⏳ Good things take time. Wait for it...", show_time=True):
        flow()
elif st.session_state.last_output is None and not st.session_state.processing:
    st.warning("✏️ Fill in your details and press 'Make my resume' to generate your CV.")
elif st.session_state.last_output is not None and not st.session_state.processing:
    st.pdf(st.session_state.last_output)
    with open(st.session_state.last_output, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        "💾 Download",
        pdf_bytes,
        file_name="cv.pdf",
        mime="application/pdf",
        use_container_width=False,
    )
else:
    st.error("Unknown state")
    st.error(st.session_state)
    st.error(st.session_state)
