FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "daphne", "-b", "0.0.0.0", "-p", "8001", "finance_management.asgi:application"]