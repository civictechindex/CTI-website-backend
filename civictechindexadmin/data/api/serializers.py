from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Organization, Link, FAQ, NotificationSubscription, Alias


class ParentOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'org_tag', 'cti_contributor', 'parent_organization']
        depth = 1
		
		
class OrganizationSerializer(serializers.ModelSerializer):
    parent_organization = ParentOrganizationSerializer(many=False, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'github_name', 'github_id', 'location', 'image_url', 'links', 'parent_organization', 'cti_contributor', 'org_tag']
        depth = 1


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'link_type', 'url', 'organization', ]
        depth = 1


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

class AddOrganizationSerializer(serializers.Serializer):
    organization_name = serializers.CharField()  # required
    parent_organization = serializers.CharField(allow_blank=True)

    website_url = serializers.URLField()  # required
    github_url = serializers.URLField()  # required

    facebook_url = serializers.URLField(allow_blank=True)
    twitter_url = serializers.URLField(allow_blank=True)
    meetup_url = serializers.URLField(allow_blank=True)

    location = serializers.CharField(allow_blank=True)
    github_tags = serializers.ChoiceField(allow_blank=True)
    organization_email = serializers.CharField()  # required

    def create(self, validated_data):
        links = [
            (Link.LINK_TYPE_CHOICES.WebSite, validated_data["website_url"]),
            (Link.LINK_TYPE_CHOICES.GitHub, validated_data["github_url"]),
            (Link.LINK_TYPE_CHOICES.FaceBook, validated_data["facebook_url"]),
            (Link.LINK_TYPE_CHOICES.Twitter, validated_data["twitter_url"]),
            (Link.LINK_TYPE_CHOICES.MeetUp, validated_data["meetup_url"]),
        ]
        try:
            org = Organization.objects.create(
                name=validated_data["organization_name"],
                parent_organization=validated_data["parent_organization"],
                location=validated_data["location"],
                org_tag=validated_data["github_tags"],
            )

            for link_type, link in links:
                if link:
                    Link.objects.create(
                        organization=org.import_id,
                        link_type=link_type,
                        url=link,
                    )
        except IntegrityError:
            raise ValidationError(detail=f"We already have a organization for {validated_data['organization_name']}")
