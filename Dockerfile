FROM python:alpine

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENV NR_API_KEY
ENV NR_ACCOUNT_ID
CMD ["python", "nrql/cli.py"]