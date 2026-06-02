FROM ghcr.io/astral-sh/uv:python3.11-alpine
WORKDIR /app

# Copiamos los archivos de configuración e instalamos dependencias
COPY pyproject.toml /app/
RUN uv sync --no-dev

# Copiamos el código del script
COPY main.py /app/

# Exponemos el puerto de la API y la levantamos
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
