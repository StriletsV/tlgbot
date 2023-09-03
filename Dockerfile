FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip install -r requrements.txt --no-cache-dir

CMD ["python", "main.py"]