ARG PYTHON_BASE=3.12-slim-bookworm
FROM python:$PYTHON_BASE AS builder

RUN pip install -U pdm
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PDM_CHECK_UPDATE=false
COPY pyproject.toml pdm.lock /code/
COPY src/ /code/src

WORKDIR /code
RUN pdm install --prod --check --no-editable

FROM python:$PYTHON_BASE

COPY --from=builder /code/.venv/ /code/.venv
ENV PATH="/code/.venv/bin:$PATH"

WORKDIR /code
COPY src ./src
CMD ["fastapi", "run", "/code/src/stakefish_test/main.py", "--port", "3000"]
