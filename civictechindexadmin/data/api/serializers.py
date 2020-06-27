from rest_framework import serializers

from civictechindexadmin.data.models import Organization, Link


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'location', 'image_url', 'links', 'parent_organization' ]
        depth = 1


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'link_type', 'url', 'organization', ]
        depth = 1
