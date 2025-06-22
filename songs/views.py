from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song
from .serializers import SongSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def get_all_songs(request):
    songs = Song.objects.all()
    
    paginator = PageNumberPagination()
    paginator.page_size = request.query_params.get('page_size')
    result_page = paginator.paginate_queryset(songs, request)

    serializer = SongSerializer(result_page, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def get_song_by_title(request):
    title = request.query_params.get('title')
    try:
        song = Song.objects.get(title=title)
        serializer = SongSerializer(song)
        return Response(serializer.data,status=200)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"}, status=404)

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

            song.star_rating = int(rating)
            song.save()

            return Response({"message": "Rating updated", "song_id": song.id, "new_rating": song.star_rating})

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    return Response({"not allowed": str(e)}, status=400)