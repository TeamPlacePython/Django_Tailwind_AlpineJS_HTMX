from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' application.

    This class sets the default auto field type for models and specifies
    the application name within the Django project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"
