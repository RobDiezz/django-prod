FROM python:3.13.2-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.0.1" && \
    poetry config virtualenvs.create false --local && \
    apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lests/*

COPY pyproject.toml poetry.lock ./mysite /app/

RUN poetry install --no-root
#    python manage.py collectstatic --noinput &&  \
#    python manage.py compilemessages

#CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]