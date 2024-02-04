import json
from fastapi.testclient import TestClient
from include import models
from include.database import get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test_data import testData
import copy

FASTAPI_SOUND_RECOMMENDER_TEST = "sqlite:///fastapi_sound_recommender_test.db"

engine = create_engine(
    FASTAPI_SOUND_RECOMMENDER_TEST, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


TEST_DATA_SOUNDS_COUNT = len(testData["sounds"])
TEST_DATA_PLAYLISTS_COUNT = len(testData["playlists"])
TEST_DATA_SOUNDS_ADDED = 0
TEST_DATA_PLAYLISTS_ADDED = 0
TEST_DATA_ADD_SOUND_IDS = []
TEST_DATA_ADD_PLAYLIST_IDS = []


def test_start():
    # create all the tables in test db
    models.Base.metadata.create_all(bind=engine)


def test_sounds_list__empty_db():
    response = client.get("/sounds/")
    assert response.status_code == 200
    response = response.json()
    assert len(response["data"]) == 0
    assert response["pagination"]["total_records"] == 0
    assert response["pagination"]["count"] == 0
    assert response["pagination"]["limit"] == 10
    assert response["pagination"]["offset"] == 0


def test_admin_init():
    response = client.get("/admin/init")
    assert response.status_code == 201
    response = response.json()
    TEST_DATA_SOUNDS_ADDED = response["data"]["sounds_added"]
    TEST_DATA_PLAYLISTS_ADDED = response["data"]["playlists_added"]
    assert TEST_DATA_SOUNDS_ADDED == TEST_DATA_SOUNDS_COUNT
    assert TEST_DATA_PLAYLISTS_ADDED == TEST_DATA_PLAYLISTS_COUNT


def test_sounds_list():
    response = client.get("/sounds?limit=5&offset=2")
    assert response.status_code == 200
    response = response.json()
    assert len(response["data"]) == 5
    assert response["pagination"]["total_records"] == TEST_DATA_SOUNDS_COUNT
    assert response["pagination"]["count"] == 5
    assert response["pagination"]["limit"] == 5
    assert response["pagination"]["offset"] == 2


def test_sounds_list__out_of_bound():
    offset = TEST_DATA_SOUNDS_COUNT+5
    response = client.get(f"/sounds?limit=5&offset={offset}")
    assert response.status_code == 200
    response = response.json()
    assert len(response["data"]) == 0
    assert response["pagination"]["total_records"] == TEST_DATA_SOUNDS_COUNT
    assert response["pagination"]["count"] == 0
    assert response["pagination"]["limit"] == 5
    assert response["pagination"]["offset"] == offset


def test_sounds_list__negative_params():
    response = client.get("/sounds?limit=-5&offset=-20")
    assert response.status_code == 422


def test_sounds_add__missing_param():
    response = client.post("/admin/sounds")
    assert response.status_code == 422


def test_sounds_add__empty_title():
    testDataTemp = copy.deepcopy(testData["add_sound"])
    testDataTemp["data"][0]["title"] = ""
    response = client.post(
        "/admin/sounds", content=json.dumps(testDataTemp))
    assert response.status_code == 400


def test_sounds_add():
    response = client.post(
        "/admin/sounds", content=json.dumps(testData["add_sound"]))
    assert response.status_code == 201
    response = response.json()
    assert len(response["data"]) == len(testData["add_sound"]["data"])
    for idx in range(0, len(response["data"])):
        TEST_DATA_ADD_SOUND_IDS.append(response["data"][idx]["id"])
        assert response["data"][idx]["title"] == testData["add_sound"]["data"][idx]["title"]


def test_playlist_add__missing_param():
    response = client.post("/playlists")
    assert response.status_code == 422


def test_playlist_add__empty_title():
    testDataTemp = copy.deepcopy(testData["add_playlist"])
    testDataTemp["data"][0]["title"] = ""
    response = client.post(
        "/admin/sounds", content=json.dumps(testDataTemp))
    assert response.status_code == 422


def test_playlist_add__empty_sounds():
    response = client.post(
        "/playlists", content=json.dumps(testData["add_playlist"]))
    assert response.status_code == 201
    response = response.json()
    assert len(response["data"]) == len(testData["add_playlist"]["data"])
    for idx in range(0, len(response["data"])):
        assert response["data"][idx]["title"] == testData["add_playlist"]["data"][idx]["title"]


def test_playlist_add():
    testData["add_playlist"]["data"][0]["sounds"] = TEST_DATA_ADD_SOUND_IDS
    response = client.post(
        "/playlists", content=json.dumps(testData["add_playlist"]))
    assert response.status_code == 201
    response = response.json()
    assert len(response["data"]) == len(testData["add_playlist"]["data"])
    for idx in range(0, len(response["data"])):
        TEST_DATA_ADD_PLAYLIST_IDS.append(response["data"][idx]["id"])
        assert response["data"][idx]["title"] == testData["add_playlist"]["data"][idx]["title"]


def test_sounds_get__missing_param():
    response = client.get("/sounds/get")
    assert response.status_code == 422


def test_sounds_get__empty_id():
    response = client.get("/sounds/get?soundId=")
    assert response.status_code == 400


def test_sounds_get__non_existing_id():
    response = client.get("/sounds/get?soundId=12345677890")
    assert response.status_code == 404


def test_sounds_get():
    soundId = TEST_DATA_ADD_SOUND_IDS[0]
    response = client.get(f"/sounds/get?soundId={soundId}")
    assert response.status_code == 200
    response = response.json()
    assert len(response["data"]) == 1
    assert response["data"][0]["title"] == testData["add_sound"]["data"][0]["title"]


def test_sounds_recommended__missing_param():
    response = client.get(f"/sounds/recommended")
    assert response.status_code == 422


def test_sounds_recommended__empty_id():
    response = client.get(f"/sounds/recommended?playlistId=")
    assert response.status_code == 400


def test_sounds_recommended__non_existing_id():
    response = client.get(f"/sounds/recommended?playlistId=1234567890")
    assert response.status_code == 404


def test_sounds_recommended():
    playlistId = TEST_DATA_ADD_PLAYLIST_IDS[0]
    response = client.get(f"/sounds/recommended?playlistId={playlistId}")
    assert response.status_code == 200
    response = response.json()
    assert response["data"][0]["title"] != ""


def test_finish():
    # delete all the tables from test db
    models.Base.metadata.drop_all(bind=engine)
