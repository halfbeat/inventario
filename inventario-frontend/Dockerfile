ARG REPO_PREFIX=""
FROM ${REPO_PREFIX}nginx:1.25.4-alpine

ARG GIT_COMMIT=unspecified
LABEL org.opencontainers.image.revision=$GIT_COMMIT

COPY build /usr/share/nginx/html/familias/gestion/
COPY dist/ciudadanos /usr/share/nginx/html/familias/ciudadanos/
COPY ./config/set_config_ciudadanos.sh /docker-entrypoint.d/40-set_config_ciudadanos.sh
COPY ./config/set_config_gestion.sh /docker-entrypoint.d/41-set_config_gestores.sh
RUN chmod u+x /docker-entrypoint.d/40-set_config_ciudadanos.sh
RUN chmod u+x /docker-entrypoint.d/41-set_config_gestores.sh
COPY ./config/nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir /usr/share/nginx/html/config
RUN chmod 777 /usr/share/nginx/html/config
EXPOSE 80
VOLUME /usr/share/nginx/html
STOPSIGNAL SIGTERM
