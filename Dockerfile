FROM python:3.11-slim as python-base 

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libopenblas-dev \
    libportaudio2 \
    portaudio19-dev

# Upgrade pip and install wheel, setuptools
RUN pip install --upgrade pip setuptools wheel

# Install llvmlite and scipy using pip
RUN pip install llvmlite scipy

# Install Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3
# RUN pip install poetry

# Install pyaudio and other dependencies
RUN pip install --no-cache-dir pyaudio==0.2.14

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-root --no-dev

FROM builder-base as development
RUN poetry install --no-root
COPY . .
RUN poetry install

CMD ["python","-m", "myapplication.main"]

FROM python-base as production

COPY --from=builder-base $VENV_PATH $VENV_PATH
WORKDIR $PYSETUP_PATH
COPY ./myapplication/ ./myapplication/
USER 10000

CMD ["python","-m", "myapplication.main"]
