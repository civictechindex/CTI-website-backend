from django.contrib import admin
from .models import Organization, Link

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization


class LinkAdmin(admin.ModelAdmin):
    model = Link


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Link, LinkAdmin)
