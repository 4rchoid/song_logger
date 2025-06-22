import pytest
from rest_framework.test import APIClient
from songs.models import Song

pytestmark = pytest.mark.django_db
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_song():
    def _create_song(title="Hey Jude", star_rating=4, song_id="s001"):
        return Song.objects.create(title=title, star_rating=star_rating, song_id=song_id)
    return _create_song

@pytest.mark.django_db
def test_create_song(create_song):
    song = create_song()
    assert song.title == "Hey Jude"
    
def test_get_all_songs(api_client, create_song):
    create_song()
    response = api_client.get('/api/songs/?page_size=5')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) <= 5

def test_get_song_by_title_success(api_client, create_song):
    song = create_song(title="Let It Be")
    response = api_client.get('/api/song_by_title/?title=Let It Be')
    assert response.status_code == 200
    assert response.data['title'] == "Let It Be"

def test_get_song_by_title_not_found(api_client):
    response = api_client.get('/api/song_by_title/?title=Nonexistent')
    assert response.status_code == 404
    assert response.data['error'] == "Song not found"

def test_patch_song_rating_success(api_client, create_song):
    song = create_song(song_id="s004", star_rating=3)
    response = api_client.patch(f'/api/rate_song/{song.song_id}/', {'rating': 5}, format='json')
    assert response.status_code == 200
    assert response.data['new_rating'] == 5

def test_patch_song_rating_invalid(api_client, create_song):
    song = create_song(song_id="s005")
    response = api_client.patch(f'/api/rate_song/{song.song_id}/', {'rating': 8}, format='json')
    assert response.status_code == 400
    assert "star_rating must be between 1 and 5" in response.data['error']

def test_patch_song_not_found(api_client):
    response = api_client.patch('/api/rate_song/s999/', {'rating': 4}, format='json')
    assert response.status_code == 404
    assert response.data['error'] == "Song not found"
