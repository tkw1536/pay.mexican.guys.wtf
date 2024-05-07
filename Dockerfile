# image for python
FROM python:3.11-alpine

# create www-data
RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

# Install binary python dependencies
RUN apk add --no-cache \
    build-base \
    linux-headers \
    python3-dev \
    mailcap

ADD docker/uwsgi.ini /app/uwsgi.ini

# Add requirements and install dependencies
ADD requirements.txt /app/
ADD requirements-prod.txt /app/
WORKDIR /app/

# install all the python runtime dependencies
RUN mkdir -p /var/www/static/ \
    && pip install -r requirements.txt \
    && pip install -r requirements-prod.txt

# Install Django App and setup the setting module
ADD manage.py /app/
ADD docker/ /app/docker
ADD pay_mexican_guys/ /app/pay_mexican_guys

# default settings are in MemberManagement
ENV DJANGO_SETTINGS_MODULE "pay_mexican_guys.docker_settings"

### ALL THE CONFIGURATION

# The secret key used for django
ENV DJANGO_SECRET_KEY ""

# A comma-seperated list of allowed hosts
ENV DJANGO_ALLOWED_HOSTS "localhost"

# Database settings
## Use SQLITE out of the box
ENV DJANGO_DB_ENGINE "django.db.backends.sqlite3"
ENV DJANGO_DB_NAME "/data/db.sqlite3"
ENV DJANGO_DB_USER ""
ENV DJANGO_DB_PASSWORD ""
ENV DJANG_DB_HOST ""
ENV DJANGO_DB_PORT ""

# create data volume, and collect static files
RUN mkdir /data/ && chown -R www-data:www-data /data/
RUN DJANGO_SECRET_KEY=setup python manage.py collectstatic --noinput

# Volume and ports
USER www-data:www-data
VOLUME /data/
EXPOSE 8080

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/app/docker/uwsgi.ini"]