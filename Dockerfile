FROM python:3.9.16-alpine
LABEL maintainer="ds-muzalevskiy"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "-u", "slackbot.py"]
