from django.db import models

# Create your models here.

class Song(models.Model):
    song_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)

    danceability = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    key = models.IntegerField(default=0)
    loudness = models.FloatField(default=0.0)
    mode = models.IntegerField(default=1)  # assuming 1 = major, 0 = minor
    acousticness = models.FloatField(default=0.0)
    instrumentalness = models.FloatField(default=0.0)
    liveness = models.FloatField(default=0.0)
    valence = models.FloatField(default=0.0)
    tempo = models.FloatField(default=120.0)

    duration_ms = models.IntegerField(default=180000)
    time_signature = models.IntegerField(default=4)
    num_bars = models.IntegerField(default=0)
    num_sections = models.IntegerField(default=0)
    num_segments = models.IntegerField(default=0)
    classification = models.IntegerField(default=0)
    
    star_rating = models.IntegerField(default=3)

    def __str__(self):
            return f"{self.title} ({self.song_id})"