FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias para PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Recopilar estáticos al construir la imagen
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "core_finanzas.wsgi:application", "--bind", "0.0.0.0:8000"]

