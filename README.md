# tutum-stream

## Install

docker build -t tutuum_stream .

## Run

Env properties to be set

TUTUM_TOKEN
TUTUM_USERNAME
HIPCHAT_URL
HIPCHAT_TOKEN
HIPCHAT_ROOM
STACK_NAME [optional]
CONTAINER_MSG [optional] - toggle container related messages on (off by default)

docker run -it -e TUTUM_TOKEN=<> ... tuutum_stream
