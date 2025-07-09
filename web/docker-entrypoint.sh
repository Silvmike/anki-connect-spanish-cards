#!/bin/sh

envsubst '${NGINX_PORT} ${IMAGE_SEARCH_SERVICE_PORT} ${TRANSLATE_SERVICE_PORT} ${AUDIO_SERVICE_PORT} ${LLM_SERVICE_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'