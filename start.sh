#!/bin/bash
app="portfolio"
docker build -t ${app} .
docker run -p 8081:80 \
  --name=${app} \
  -v "$PWD:/app" ${app}
wait
docker stop ${app}
docker rm ${app}