from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DataConfig(AppConfig):
    name = "civictechindexadmin.data"
    verbose_name = _("Data")

    def ready(self):
        try:
            import civictechindexadmin.data.signals  # noqa F401
        except ImportError:
            pass
