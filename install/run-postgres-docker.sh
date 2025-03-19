#!/bin/sh

PORT="${1:-5432}"
docker run -p ${PORT}:5432 -it -v ./pgdata:/var/lib/postgresql/data -e POSTGRES_USER=admin -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_PASSWORD=secret postgres:17