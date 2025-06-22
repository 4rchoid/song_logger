import logging
import traceback
from django.http import JsonResponse

class ServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            # Log the full traceback
            self.logger.error("Unhandled Exception", exc_info=True)

            # Return a structured JSON response
            return JsonResponse(
                {
                    "error": "A server error occurred. Please try again later.",
                    "details": str(e),  # Optional: remove this in production for security
                },
                status=500
            )
