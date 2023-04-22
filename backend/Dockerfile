FROM python:3.11-slim
# Requirements for `psycorg2` and script "/app/run_app.sh".
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat
# It also create directory `/app`.
WORKDIR /app
COPY requirements.txt ./
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod +x run_app.sh
ENTRYPOINT ["/app/run_app.sh"]