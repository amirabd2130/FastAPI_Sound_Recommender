# FastAPI_Sound_Recommender v1.0.0

A simple sound library API implemented using FastAPI. The available endpoints are:

- **GET**: `/admin/init`: Reads the sample data from `test_data.py` and populates the database.

- **DELETE**: `/admin/cleanup`: Deletes all data from the database.

- **POST**: `/admin/sounds`: Adds a list of sounds to the database.

- **POST**: `/playlists`: Adds a new playlist to the database.

- **GET**: `/sounds` Returns a list of existing sounds. Optional parameters include `limit` (default 10) to specify the maximum records to return and `offset` (default 0) to specify the starting point. Records are sorted in ascending order by their `title`.

- **GET**: `/sounds/{id}` Searchs and returns a sound by it's `id`

- **GET**: `/sounds/recommended` Returns a random sound from a playlist using the provided `playlistId`.

**NOTE**: `/admin/init` and `/admin/cleanup` are included to facilitate testing.

# Running Locally

## Running Outside docker

The Following environment variable must be set if you want to execute the API outside docker.

```sh
export FASTAPI_SOUND_RECOMMENDER_DATABASE_URL=sqlite:///fastapi_sound_recommender.db
```

Navigate to `FastAPI_Sound_Recommender` directory and execute the following command:

```sh
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

OR

```sh
uvicorn main:app --port 8080
```

## Running Using `docker compose`

Navigate to `FastAPI_Sound_Recommender` directory and execute the following command:

```sh
docker compose up --build
```

## Swagger Documentation & Testing

You can test the service using the Swagger documentation accessible below.

http://127.0.0.1:8080/docs

# Tests

Navigate to `FastAPI_Sound_Recommender` directory and run the following command to execute all the tests:

```sh
python3 -m pytest
```
