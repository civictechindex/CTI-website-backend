from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Organization, Link, FAQ, NotificationSubscription, Alias


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'link_type', 'url', ]
        depth = 1


class ParentOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_tag', 'cti_contributor', 'parent_organization']
        depth = 1


class OrganizationSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'github_name', 'github_id', 'image_url',
                  'city', 'state', 'country', 'cti_contributor', 'org_tag',
                  'organization_email', ]


class OrganizationFullSerializer(serializers.ModelSerializer):
    parent_organization = ParentOrganizationSerializer(many=False, read_only=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'github_name', 'github_id', 'image_url',
                  'city', 'state', 'country', 'cti_contributor', 'org_tag',
                  'organization_email', 'links', 'parent_organization', ]
        depth = 1


class AddOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)  # required
    parent_organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False)

    website_url = serializers.URLField(max_length=1024, required=False)
    github_url = serializers.URLField(max_length=1024)  # required
    facebook_url = serializers.URLField(max_length=1024, required=False)
    twitter_url = serializers.URLField(max_length=1024, required=False)
    meetup_url = serializers.URLField(max_length=1024, required=False)

    city = serializers.CharField(max_length=512, required=False)
    state = serializers.CharField(max_length=512, required=False)
    country = serializers.CharField(max_length=512, required=False)
    org_tag = serializers.CharField(max_length=128)
    organization_email = serializers.EmailField(max_length=128)  # required - but not in our data model

    def create(self):
        validated_data = self.validated_data
        links = [
            ('WebSite', validated_data.get('website_url')),
            ('GitHub', validated_data.get('github_url')),
            ('FaceBook', validated_data.get('facebook_url')),
            ('Twitter', validated_data.get('twitter_url')),
            ('MeetUp', validated_data.get('meetup_url')),
        ]
        try:
            org = Organization.objects.create(
                name=validated_data["name"],
                parent_organization=validated_data.get("parent_organization", None),
                city=validated_data.get('city', None),
                state=validated_data.get('state', None),
                country=validated_data.get('country', None),
                org_tag=validated_data['org_tag'],
                organization_email=validated_data['organization_email'],
            )
        except IntegrityError as e:
            raise ValidationError(detail=e)

        for link_type, link in links:
            if link:
                Link.objects.create(
                    organization=org,
                    link_type=link_type,
                    url=link,
                )
        return org


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'view_count', ]
        depth = 1


class AliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = ['id', 'tag', 'alias', ]
        depth = 1


class NotificationSubscriptionSerializer(serializers.Serializer):
    email_address = serializers.EmailField()
    notification_type = serializers.CharField()
    created_date = serializers.DateTimeField(read_only=True)
    ip_address = serializers.IPAddressField(read_only=True)

    def create(self, validated_data):
        try:
            return NotificationSubscription.objects.create(**validated_data)
        except IntegrityError:
            raise ValidationError(detail=f"We already have a subscription for {validated_data['email_address']}")
