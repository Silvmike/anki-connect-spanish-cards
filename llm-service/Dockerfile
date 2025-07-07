FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
RUN pip install transformers==4.41.0 --no-cache-dir
RUN pip install packaging ninja --no-cache-dir
RUN pip install https://github.com/Dao-AILab/flash-attention/releases/download/v2.6.2/flash_attn-2.6.2+cu118torch2.3cxx11abiFALSE-cp312-cp312-linux_x86_64.whl
RUN pip install --no-cache-dir uvicorn fastapi pydantic
RUN pip install --no-cache-dir accelerate[torch]

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD ["python", "llm-service.py"]