# Tweak the base image by installing pipenv and GNU gettext tools
FROM python:3.11 as base
RUN pip install pipenv

# Begin our actual build
FROM base as base1
# collectstatic needs the secret key to be set. We store that in this environment variable.
# Set this value in this project's .env file
ARG DJANGO_SECRET_KEY

RUN mkdir -p /usr/src/app

COPY ./_app /usr/src/app
COPY Pipfile /usr/src/app/
COPY Pipfile.lock /usr/src/app/

WORKDIR /usr/src/app

# Install gettext using the system package manager
RUN apt-get update && apt-get install -y gettext

RUN pipenv install --system --deploy
RUN python manage.py collectstatic --no-input
