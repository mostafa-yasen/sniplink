from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from shortener.serializers import ShortenedURLSerializer
from shortener.models import ShortenedURL


class ShortenedURLViewSet(ModelViewSet):
    """
    ViewSet for managing shortened URLs.
    Provides CRUD operations plus custom stats endpoint.
    """

    lookup_field = "short_code"
    serializer_class = ShortenedURLSerializer
    queryset = ShortenedURL.objects.all()
    lookup_url_kwarg = "short_code"

    @action(detail=True, methods=["get"], url_path="stats")
    def stats(self, request, short_code=None):
        """
        Custom endpoint: GET /shorten/{short_code}/stats
        Returns the same data as retrieve but semantically different.
        """
        url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
        serializer = self.get_serializer(url_obj)
        return Response(serializer.data)


class RedirectView(APIView):
    """
    View for redirecting to the original URL.
    """

    def get(self, request, short_code: str | None = None):
        """
        Custom endpoint: GET /{short_code}
        Redirects to the original URL.
        """
        url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
        url_obj.increment_access_count()
        return redirect(url_obj.url)
