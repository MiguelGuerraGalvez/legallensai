FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend/

RUN useradd -m myuser

RUN chown -R myuser:myuser /backend
USER myuser

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]