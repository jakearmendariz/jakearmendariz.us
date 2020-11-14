#!/bin/bash
app="flask"
docker build -t ${app} .
docker run -p 5000:80 \
  --name=${app} \
  -v "$PWD:/app" ${app}
wait
docker stop ${app}
docker rm ${app}