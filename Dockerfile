FROM --platform=linux/amd64 python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    HF_HOME="/tmp/huggingface_cache"

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
    portaudio19-dev \
    libasound2-dev \
    libjack-dev

RUN dpkg -l libportaudio2 portaudio19-dev
RUN find / -name libportaudio.so.2
RUN cp /usr/lib/*/libportaudio.so.2 /usr/lib/
RUN ldconfig

# Find and copy required libraries to a known location
RUN mkdir -p /usr/local/lib/audiolibs && \
    find /usr/lib -name "libportaudio.so*" -exec cp {} /usr/local/lib/audiolibs/ \; && \
    find /usr/lib -name "libasound.so*" -exec cp {} /usr/local/lib/audiolibs/ \; && \
    find /usr/lib -name "libjack.so*" -exec cp {} /usr/local/lib/audiolibs/ \;

# In the builder-base stage
RUN apt-get update && apt-get install -y git
RUN pip3 install picovoice
RUN pip install pvporcupine
# Upgrade pip and install wheel, setuptools
RUN pip install --upgrade pip setuptools wheel
# Install pyaudio and other dependencies
RUN pip install pyaudio
# Install llvmlite and scipy using pip
RUN pip install llvmlite scipy

# Install Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3

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
COPY --from=builder-base /usr/local/lib/audiolibs/ /usr/lib/

WORKDIR $PYSETUP_PATH
COPY ./myapplication/ ./myapplication/

# # Add execute permissions and change ownership
RUN chmod +x /usr/lib/libportaudio.so* /usr/lib/libasound.so* /usr/lib/libjack.so* && \
    chown 10000:10000 /usr/lib/libportaudio.so* /usr/lib/libasound.so* /usr/lib/libjack.so*
RUN mkdir -p /tmp/huggingface_cache && chmod 777 /tmp/huggingface_cache

# Update the shared library cache
RUN ldconfig

USER 10000

CMD ["python","-m", "myapplication.main"]
