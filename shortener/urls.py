from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shortener.views import ShortenedURLViewSet, RedirectView

router = DefaultRouter()
router.register(r"shorten", ShortenedURLViewSet, basename="shortenedurl")

urlpatterns = [
    path("api/", include(router.urls)),
    path("<str:short_code>/", RedirectView.as_view(), name="redirect"),
]
