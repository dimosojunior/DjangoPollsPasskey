
#!/bin/sh

set -x
echo Starting app
env

exec uvicorn --host $BIND_ADDRESS --port $LISTEN_PORT --log-level $PYTHON_LOG_LEVEL main:app
