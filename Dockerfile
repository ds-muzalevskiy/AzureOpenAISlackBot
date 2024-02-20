FROM python:3.10-alpine
LABEL maintainer="ds-muzalevskiy"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["slackbot_chatgpt.py"]
