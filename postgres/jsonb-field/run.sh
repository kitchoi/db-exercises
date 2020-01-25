#!/usr/bin/bash

POSTGRES_PASSWORD=postgres
PGPASSWORD=postgres
echo $PGPASSWORD
docker stop postgres-jsonb && docker container rm postgres-jsonb
docker run --name postgres-jsonb -p 1234:5432 -d postgres
sleep 5
psql -h 0.0.0.0 -p 1234 -U postgres -a -f script.sql
