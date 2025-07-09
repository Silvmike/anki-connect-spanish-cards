# Use official nginx image as base
FROM nginx:alpine

# Install required tools
RUN apk add --no-cache gettext openssl apache2-utils
# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Create directories for SSL and auth
RUN mkdir -p /etc/nginx/ssl && mkdir -p /var/www/html

# Generate self-signed SSL certificates (valid for 1 year)
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -subj "/C=US/ST=California/L=San Francisco/O=Your Company/CN=localhost" \
    -addext "subjectAltName=DNS:localhost"

# Arguments for basic auth
ARG AUTH_USERNAME=admin
ARG AUTH_PASSWORD=defaultpassword
ENV AUTH_USERNAME=$AUTH_USERNAME
ENV AUTH_PASSWORD=$AUTH_PASSWORD

# Create .htpasswd with build-time credentials
RUN htpasswd -nb "$AUTH_USERNAME" "$AUTH_PASSWORD" > /etc/nginx/.htpasswd && \
    chmod 644 /etc/nginx/.htpasswd

# Copy your nginx config template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Copy your static files (if any)
COPY static/ /var/www/html/

# Environment variables with default values
ENV NGINX_PORT=443
ENV IMAGE_SEARCH_SERVICE_PORT=8001
ENV TRANSLATE_SERVICE_PORT=8002
ENV AUDIO_SERVICE_PORT=8003
ENV LLM_SERVICE_PORT=8004

# Script to substitute environment variables and start nginx
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]