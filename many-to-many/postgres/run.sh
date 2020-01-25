#!/usr/bin/bash

TAG="9.6"
PORT=1234
NAME="postgres_many_to_many"
POSTGRES_PASSWORD=postgres
PGPASSWORD=postgres
echo $PGPASSWORD
docker stop $NAME && docker container rm $NAME
docker run --name $NAME -p $PORT:5432 -d postgres:$TAG
sleep 5
echo "Running at port: $PORT"
read -n 1 -p "Continue?"
docker stop $NAME && docker container rm $NAME