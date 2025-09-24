from django.db import IntegrityError, models
from django.core.validators import MinValueValidator
import secrets
import string


class ShortenedURL(models.Model):
    RESERVED_WORDS = {
        # Django built-ins
        "admin",
        "static",
        "media",
        "api",
        # Our app paths
        "shorten",
        "stats",
        # Common web files
        "robots",
        "favicon",
        "sitemap",
        "manifest",
        # Web standards
        "www",
        "ftp",
        "http",
        "https",
        "mail",
        "email",
        # Potentially confusing
        "null",
        "undefined",
        "error",
        "test",
        "demo",
        "sample",
        # Common app routes
        "login",
        "logout",
        "register",
        "signup",
        "signin",
        "home",
        "index",
        "about",
        "contact",
        "help",
        "support",
        # Short variations to avoid confusion
        "app",
        "web",
        "dev",
        "prod",
        "staging",
    }
    url = models.URLField(
        max_length=2048,
        help_text="The original long URL to be shortened",
    )
    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="The unique short code for the URL",
    )

    access_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of times this short URL has been accessed",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.url}"

    @classmethod
    def is_valid_short_code(cls, short_code: str) -> bool:
        """Check if a short code is valid (not reserved)"""
        return short_code.lower() not in cls.RESERVED_WORDS

    @classmethod
    def generate_short_code(
        cls,
        url: str,
        length: int = 6,
        max_attempts: int = 100,
    ) -> "ShortenedURL":
        """Generate a random short code that does not exist in the database."""
        characters = string.ascii_letters + string.digits
        err_msg = "Unable to generate a unique short code after maximum attempts."
        for attempt in range(max_attempts):
            short_code = "".join(secrets.choice(characters) for _ in range(length))
            if not cls.is_valid_short_code(short_code):
                continue

            try:
                return cls.objects.create(url=url, short_code=short_code)
            except IntegrityError:
                if attempt >= max_attempts - 1:
                    raise ValueError(err_msg)
                continue
        raise ValueError(err_msg)

    def increment_access_count(self) -> None:
        """Increment the access count by 1."""
        from django.db.models import F

        self.__class__.objects.filter(pk=self.pk).update(
            access_count=F("access_count") + 1
        )

        self.refresh_from_db(fields=["access_count"])
