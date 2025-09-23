from rest_framework import serializers
from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    """
    Serializer for ShortenedUrl model.
    - Accepts only 'url' field for input (creation/updates)
    - Returns all fields for output (retrieval)
    """

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "url",
            "short_code",
            "access_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "short_code",
            "access_count",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Override create to use our collision-handling method."""
        url = validated_data["url"]
        return ShortenedURL.create_with_short_code(url)


class UrlStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for UrlStats model.
    - Returns all fields for output (retrieval)
    """

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "url",
            "access_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = "__all__"
