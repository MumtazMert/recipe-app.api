FROM python:3.9-alpine3.13
#This is defining who is maintaining the project
LABEL maintainer="MumtazMert"

#It tells python to dont buffer.We can see the logs immidiately
ENV PYTHONUNBUFFERED 1

#This parts copies our requirements to the docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
#Default directory to run our commands
WORKDIR /app
#Exposes the port number
EXPOSE 8000

ARG DEV=false

#Creating Virtual env and specifing home path for our project
RUN python -m venv /py&& \
    /py/bin/pip install --upgrade pip && \
    #İnstalling postgresql client
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    #Shell command 
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    #------------------------
    rm -rf /tmp && \
    #We removed build deps.It keeps docker file lightweight and clean
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
 #Defines all of the directories which executables can be run
ENV PATH="/py/bin:$PATH"
# Specifies the user to be
USER django-user