from django.apps import AppConfig


class MokuConfig(AppConfig):
    """Django application configuration for moku.blog."""

    name = "moku"
    label = "moku"
    verbose_name = "moku.blog"

    def ready(self):
        from pi_heif import register_heif_opener

        register_heif_opener()
