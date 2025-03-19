#!/bin/sh

PORT="${1:-6379}"
docker run -p ${PORT}:6379 -it redis/redis-stack:latest