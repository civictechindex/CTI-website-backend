from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Organization, Link

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('import_id', 'name', 'location', 'parent_organization')
    list_display_links = ('name', )
    search_fields = ('name', 'location')


class LinkAdmin(admin.ModelAdmin):
    model = Link
    list_display = ('id', 'link_type', 'display_url')
    list_display_links = ('id', )
    list_filter = ('link_type', )

    def display_url(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Link, LinkAdmin)
