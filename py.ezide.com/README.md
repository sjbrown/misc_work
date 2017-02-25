# Dockerized Flask with uWSGI and NGINX

## Development environment

 * `docker-compose -f docker-compose.yml -f docker-compose.developer.yml up`

While developing you will want to see debug output, and you will want to make
changes to the Python files in `app/` and see them reflected immediately.

The development environment doesn't allow multiple connections though.

It is available on `http://localhost:8877`.


## Production environment

 * `docker-compose up`

This runs via NGINX - uWSGI - Flask.

It is available on `http://localhost:80`.


----

Acknowledgements:

 * https://github.com/tiangolo/uwsgi-nginx-flask-docker
