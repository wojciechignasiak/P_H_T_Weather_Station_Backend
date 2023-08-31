#pull official base image
FROM python:3.11-alpine

# set working directory
WORKDIR /usr/src/pht_backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update \
    && apk upgrade
RUN apk add bash

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod a+x /usr/src/pht_backend/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/pht_backend/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]