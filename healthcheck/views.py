# core/views.py
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

@api_view(['GET'])
def health_check(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return JsonResponse({'status': 'fail', 'database': 'unreachable'}, status=500)

    return JsonResponse({'status': 'ok', 'database': 'reachable'})
