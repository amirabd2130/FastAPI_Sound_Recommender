FROM python:3.11

# ensure `.pyc` files will not be created
ENV PYTHONDONTWRITEBYTECODE 1
# this keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1
# ensure `pip` does not use a cache directory
ENV PIP_NO_CACHE_DIR 1

# create a non-root user `python:python`
RUN groupadd --gid 1000 python && useradd --uid 1000 --gid python --shell /bin/bash --create-home python

# create app directory
RUN mkdir -p /home/python/app
WORKDIR /home/python/app

# copy files
COPY . .
RUN chown -R python:python /home/python/app

# update pip and install dependencies
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

USER 1000
# CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]
