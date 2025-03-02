FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y chromium chromium-driver libjpeg-dev zlib1g-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
