from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Organization, Link, FAQ, NotificationSubscription


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


class FAQAdmin(admin.ModelAdmin):
    model = FAQ
    list_display = ('id', 'live', 'question',)
    list_filter = ('live',)
    search_fields = ('question', 'answer')


class NotificationSubscriptionAdmin(admin.ModelAdmin):
    model = NotificationSubscription
    list_display = ('email_address', 'notification_type', 'ip_address', 'created_date')
    search_fields = ('email_address', )


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(NotificationSubscription, NotificationSubscriptionAdmin)
