#!/usr/bin/bash

POSTGRES_PASSWORD=postgres
PGPASSWORD=postgres
CONTAINER_NAME=postgres-toy
echo $PGPASSWORD
docker stop $CONTAINER_NAME && docker container rm $CONTAINER_NAME
docker run --name $CONTAINER_NAME -p 5432:5432 -d postgres
sleep 5
psql -h 0.0.0.0 -p 5432 -U postgres -a -f postgres_setup.sql
read -n 1 -p "Continue?"
docker stop $CONTAINER_NAME && docker container rm $CONTAINER_NAME
