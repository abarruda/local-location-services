FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
  nginx 

COPY nginx_config/local-location-services /etc/nginx/sites-available/default
COPY dist/ /local-location-services/dist/

EXPOSE 80

CMD nginx -g "daemon off;"
