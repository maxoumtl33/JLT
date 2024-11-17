from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'listings'

    def ready(self):
        import listings.signals  # Replace with your actual app name
