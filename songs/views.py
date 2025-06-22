from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Song
from .serializers import SongSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_all_songs(request):

    songs = Song.objects.all()
    if not songs.exists():
        return Response({"error": "No songs found."}, status=404)


    try:
        page_size = int(request.query_params.get('page_size', 10))  # Page size
        page = int(request.query_params.get('page', 1))  # Page number
        if page_size <= 0 or page <= 0:
            raise ValueError
    except ValueError:
        return Response(
            {"error": "Invalid 'page' or 'page_size'. Must be positive integers."},
            status=status.HTTP_400_BAD_REQUEST
        )
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_songs = songs[start_index:end_index]
    
    serializer = SongSerializer(paginated_songs, many=True)
    
    return Response(serializer.data)

    
@api_view(['GET'])
def get_song_by_title(request):
    title = request.query_params.get('title')

    if not title:
        return Response(
            {"error": "Missing or empty 'title' query parameter."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        song = Song.objects.get(title=title)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Song.DoesNotExist:
        return Response(
            {"error": f"Song not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PATCH'])
def rate_song(request,id_song):
    if request.method == 'PATCH':

        try:
            song = Song.objects.get(song_id=id_song)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=404)

        try:    
            rating = request.data.get("rating")

            if rating is None or not (1 <= int(rating) <= 5):
                return Response({"error": "star_rating must be between 1 and 5"}, status=400)

            try:
                rating = int(rating)
            except ValueError:
                return Response({"error": "Rating must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            
            song.star_rating = int(rating)
            song.save()

            return Response({"message": "Rating updated", "song_id": song.id, "new_rating": song.star_rating})

        except Exception as e:
            return Response({"error": str(e)}, status=400)