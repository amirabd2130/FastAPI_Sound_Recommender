from fastapi import FastAPI
from include import database, models
from routers import admin, playlists, sounds

DESCRIPTION = """
A simple sound library API implemented using FastAPI. The available endpoints are:

- **GET**: `/admin/init`: Reads the sample data from `test_data.py` and populates the database.

- **DELETE**: `/admin/cleanup`: Deletes all data from the database.

- **POST**: `/admin/sounds`: Adds a list of sounds to the database.

- **POST**: `/playlists`: Adds a new playlist to the database.

- **GET**: `/sounds` Returns a list of existing sounds. Optional parameters include `limit` (default 10) to specify the maximum records to return and `offset` (default 0) to specify the starting point. Records are sorted in ascending order by their `title`.

- **GET**: `/sounds/{id}` Searchs and returns a sound by it's `id`

- **GET**: `/sounds/recommended` Returns a random sound from a playlist using the provided `playlistId`.

**NOTE**: `/admin/init` and `/admin/cleanup` are included to facilitate testing.
"""

app = FastAPI(
    title="FastAPI - Sound Recommender",
    description=DESCRIPTION,
    version="1.0.0",
    contact={
        "name": "Amir Abdollahi",
        "url": "https://github.com/amirabd2130/FastAPI_Sound_Recommender",
        "email": "amirabd2130@yahoo.com",
    },
    openapi_tags=[
        {
            "name": "Admin",
            "description": "",
        },
        {
            "name": "Playlists",
            "description": "",
        },
        {
            "name": "Sounds",
            "description": "",
        },
    ],
)
app.include_router(admin.router)
app.include_router(playlists.router)
app.include_router(sounds.router)

# create tables if they don't exist in the database
models.Base.metadata.create_all(bind=database.engine)
