FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir build && python -m pip install --no-cache-dir .

COPY . .

CMD ["python", "-m", "app.main"]
