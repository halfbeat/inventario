ARG PYTHON_VERSION=3.13
ARG REPO_PREFIX=""
FROM ${REPO_PREFIX}python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG http_proxy
ARG https_proxy

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install the dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


COPY requirements.txt .
COPY src/inventario inventario
COPY src/instance instance
COPY src/config config

RUN chown -R appuser .

USER appuser

EXPOSE 80

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--log-level=debug", "--capture-output", "inventario.entrypoints.flask_app:app"]