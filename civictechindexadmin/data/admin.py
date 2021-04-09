from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Alias, FAQ, Link, NotificationSubscription, Organization
from .status_code_filter import StatusCodeFilter


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0
    fields = ('link_type', 'url', )


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name', 'cti_contributor', 'parent_organization', 'org_tag', 'status', )
    list_display_links = ('name', )
    list_filter = ('status', 'cti_contributor')
    search_fields = ('name', )
    inlines = [LinkInline]


class LinkAdmin(admin.ModelAdmin):
    model = Link
    list_display = ('id', 'link_type', 'display_url', 'http_status')
    list_display_links = ('id', )
    list_filter = ('link_type', StatusCodeFilter)
    search_fields = ('url',)

    def display_url(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


class FAQAdmin(admin.ModelAdmin):
    model = FAQ
    list_display = ('id', 'live', 'question', 'view_count', 'status',)
    list_filter = ('live', 'status',)
    search_fields = ('question', 'answer')


class AliasAdmin(admin.ModelAdmin):
    model = Alias
    list_display = ('id', 'tag', 'alias')
    list_filter = ('tag', 'alias',)
    search_fields = ('tag', 'alias')


class NotificationSubscriptionAdmin(admin.ModelAdmin):
    model = NotificationSubscription
    list_display = ('email_address', 'notification_type', 'ip_address', 'created_date')
    search_fields = ('email_address', )


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(NotificationSubscription, NotificationSubscriptionAdmin)
