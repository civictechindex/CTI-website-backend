from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(title="Civic Tech Index API Documentation",
                 default_version='v1',
                 ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    re_path(r'status/?$', TemplateView.as_view(template_name="pages/status.txt"), name="status"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("civictechindexadmin.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
