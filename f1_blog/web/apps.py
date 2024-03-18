from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'f1_blog.web'

    def ready(self):
        import f1_blog.web.signals