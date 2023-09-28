FROM python:3.11

RUN mkdir /app
WORKDIR /app
ADD ./app/ /app/
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 5000
CMD ["python3", "/app/main.py"]
