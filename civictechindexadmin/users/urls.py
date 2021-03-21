from django.urls import path
from civictechindexadmin.data.api.views import OrganizationViewById
from rest_framework.routers import DefaultRouter

from civictechindexadmin.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]

router = DefaultRouter()
router.register(r'organizations', OrganizationViewById)

app_name = "organizations"
urlpatterns = [
    #path("~organizationByName", view=OrganizationViewById, name="organizationByName"),
    path('OrganizationById/<int:pk>', OrganizationViewById),
]
