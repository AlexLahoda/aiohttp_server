FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "api_app.py"]