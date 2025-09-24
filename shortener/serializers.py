from rest_framework import serializers
from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    """
    Serializer for ShortenedUrl model.
    - Accepts only 'url' field for input (creation/updates)
    - Returns all fields for output (retrieval)
    """

    shortCode = serializers.CharField(source="short_code", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    accessCount = serializers.IntegerField(source="access_count", read_only=True)

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "url",
            "shortCode",
            "accessCount",
            "createdAt",
            "updatedAt",
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
        return ShortenedURL.generate_short_code(url)
