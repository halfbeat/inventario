#!/usr/bin/env sh

envsubst < /docker-entrypoint.d/config.js.template > /usr/share/nginx/html/inventario/config.js
