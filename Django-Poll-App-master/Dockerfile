FROM alpine:3.15.0

EXPOSE 8001

WORKDIR /app/src
COPY . .

ENV LISTEN_PORT=8001
ENV BIND_ADDRESS=0.0.0.0
ENV PYTHON_LOG_LEVEL=debug

RUN apk add python3 py3-pip

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
