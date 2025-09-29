FROM python:3.12

RUN apt-get update && apt-get install -y wget fonts-dejavu ghostscript && rm -rf /var/lib/apt/lists/*

RUN wget -O - https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

EXPOSE 8501

RUN uv sync --locked --all-groups

CMD ["uv", "run", "python", "-m", "streamlit", "run", "src/ui/streamlit.py"]
