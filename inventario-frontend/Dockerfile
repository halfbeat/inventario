ARG REPO_PREFIX=""

FROM ${REPO_PREFIX}node:14.21.2 as build-stage
ARG STAGE=local
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run-script "build:${STAGE}"

FROM ${REPO_PREFIX}nginx:1.25.4-alpine
ARG GIT_COMMIT=unspecified
LABEL org.opencontainers.image.revision=$GIT_COMMIT

COPY --from=build-stage /app/build /usr/share/nginx/html/inventario/
COPY install/set_config.sh /docker-entrypoint.d/41-set_config.sh
RUN chmod u+x /docker-entrypoint.d/41-set_config.sh
COPY install/nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir /usr/share/nginx/html/config
RUN chmod 777 /usr/share/nginx/html/config
EXPOSE 80
VOLUME /usr/share/nginx/html
STOPSIGNAL SIGTERM
