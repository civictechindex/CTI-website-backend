from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from civictechindexadmin.data.api.views import (
    OrganizationViewSet, LinkViewSet, FAQViewSet, AliasViewSet,
    subscribe
)

app_name = "api"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("organizations", OrganizationViewSet)
router.register("links", LinkViewSet)
router.register("faqs", FAQViewSet)
router.register("aliases", AliasViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('subscribe/', subscribe),
]
