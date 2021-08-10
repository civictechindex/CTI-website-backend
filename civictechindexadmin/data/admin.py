from django.contrib import admin
from django.utils.safestring import mark_safe
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Alias, FAQ, Link, NotificationSubscription, Organization, Contact
from .status_code_filter import StatusCodeFilter


class LinkInline(admin.StackedInline):
    model = Link
    extra = 0
    fields = ('link_type', 'url', )


class OrganizationAdmin(TreeAdmin):
    model = Organization
    list_display = ('id', 'name', 'cti_contributor', 'org_tag', 'status', )
    list_display_links = ('id', 'name')
    list_filter = ('status', 'cti_contributor')
    search_fields = ('name', 'city', 'state', 'country')
    form = movenodeform_factory(Organization)
    inlines = [LinkInline]


class LinkAdmin(admin.ModelAdmin):
    model = Link
    list_display = ('id', 'link_type', 'organization', 'display_url', 'http_status')
    list_display_links = ('id', )
    search_fields = ('organization__name', 'url')
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


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('id', 'email', 'text', 'name', 'organization', 'project_url')
    list_filter = ('email', 'organization')
    search_fields = ('text', 'name')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(NotificationSubscription, NotificationSubscriptionAdmin)
admin.site.register(Contact, ContactAdmin)
