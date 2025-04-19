ARG REPO_PREFIX=""

FROM ${REPO_PREFIX}node:14.21.2 as build-stage
WORKDIR /app
COPY package*.json .
RUN npm install
COPY config /app/config
COPY public /app/public
COPY scripts /app/scripts
COPY src /app/src
COPY .env* /app/
COPY tsconfig.json /app/
RUN npm run-script "build"

FROM ${REPO_PREFIX}nginx:1.25.4-alpine
ARG GIT_COMMIT=unspecified
LABEL org.opencontainers.image.revision=$GIT_COMMIT

COPY --from=build-stage /app/build /usr/share/nginx/html/inventario/
COPY install/set_config.sh /docker-entrypoint.d/41-set_config.sh
COPY install/config.js.template /docker-entrypoint.d/config.js.template
RUN chmod u+x /docker-entrypoint.d/41-set_config.sh
COPY install/nginx.conf /etc/nginx/conf.d/default.conf
COPY install/gatewayserver.crt /etc/nginx/nginx.crt
COPY install/gatewayserver.key /etc/nginx/nginx.key

EXPOSE 80
VOLUME /usr/share/nginx/html
STOPSIGNAL SIGTERM
