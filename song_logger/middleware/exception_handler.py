import traceback
from django.http import JsonResponse

class ServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            # Log the full traceback
            print("Unhandled Exception")

            # Return a structured JSON response
            return JsonResponse(
                {
                    "error": "A server error occurred. Please try again later.",
                    "details": str(e),  # Optional: remove this in production for security
                },
                status=500
            )
