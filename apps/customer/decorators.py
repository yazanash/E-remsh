
from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def group_required(*group_names):
    """
    Custom decorator to validate if the user belongs to at least one of the specified groups.
    :param group_names: The group names to check against.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return Response({'error': 'Unauthorized access. Please log in.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Check if user belongs to at least one of the required groups
            if not request.user.groups.filter(name__in=group_names).exists():
                return Response({'error': 'Forbidden. User does not have the required permissions.'},
                                status=status.HTTP_403_FORBIDDEN)

            # User is authorized, proceed to the view
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
