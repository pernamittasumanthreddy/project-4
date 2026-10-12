"""HMS Core Exception Handler — Member 1 Foundation"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """Standardized API error response format across all HMS modules."""
    response = exception_handler(exc, context)

    if response is not None:
        data = {
            'success': False,
            'status_code': response.status_code,
            'error': response.data
        }
        return Response(data, status=response.status_code)

    return Response({
        'success': False,
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'error': str(exc)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
