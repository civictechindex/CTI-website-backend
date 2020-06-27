from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from civictechindexadmin.data.api.views import OrganizationViewSet, LinkViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("organizations", OrganizationViewSet)
router.register("links", LinkViewSet)


app_name = "api"
urlpatterns = router.urls
