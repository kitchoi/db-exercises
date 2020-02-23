#!/usr/bin/bash

POSTGRES_PASSWORD=postgres
PGPASSWORD=postgres

if test -z "$NAME"
then
    NAME=postgres-toy
fi

read -n 1 -p "Reset? (y/N)" do_reset
if [ "$do_reset" == "y" ]; then
    docker stop $NAME && docker container rm $NAME
fi
docker stop $NAME && docker container rm $NAME
docker run --name $NAME -p 5432:5432 -d postgres
sleep 5
docker exec $NAME psql -c "CREATE DATABASE $NAME;" -p 5432 -U postgres
read -n 1 -p "Kill? (y/N)" do_kill
if [ "$do_kill" == "y" ]; then
    docker stop $NAME && docker container rm $NAME
fi
