#!/usr/bin/bash

POSTGRES_PASSWORD=postgres
PGPASSWORD=postgres

if test -z "$NAME"
then
    NAME=postgres-toy
fi
echo $PGPASSWORD
docker stop $NAME && docker container rm $NAME
docker run --name $NAME -p 5432:5432 -d postgres
sleep 5
docker exec $NAME psql -c "CREATE DATABASE $NAME;" -p 5432 -U postgres
read -n 1 -p "Continue?"
docker stop $NAME && docker container rm $NAME
