from django.apps import AppConfig

class SearchIndexesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search_indexes"

    def ready(self):
        import search_indexes.signals
