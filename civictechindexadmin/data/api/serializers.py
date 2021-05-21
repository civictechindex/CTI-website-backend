import re

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from ..models import Organization, Link, FAQ, NotificationSubscription, Alias


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'link_type', 'url']
        depth = 1


class OrganizationSerializer(serializers.ModelSerializer):
    affiliated = serializers.SerializerMethodField()
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'depth', 'path', 'name', 'slug', 'github_name', 'github_id',
                  'cti_contributor', 'city', 'state', 'country', 'image_url', 'org_tag',
                  'affiliated', 'links', ]

    def get_affiliated(self, org):
        return not (org.depth == 2 and org.numchild == 0)


class OrganizationFullSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)
    aliases = serializers.SerializerMethodField()
    affiliated = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'depth', 'path', 'name', 'slug', 'github_name', 'github_id',
                  'cti_contributor', 'city', 'state', 'country', 'image_url', 'org_tag',
                  'links', 'aliases', 'affiliated', ]

    def get_aliases(self, org):
        return [a.alias for a in Alias.objects.filter(tag=org.org_tag).all()]

    def get_affiliated(self, org):
        return not (org.depth == 2 and org.numchild == 0)


class AddOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=256,
        validators=[UniqueValidator(
            queryset=Organization.objects.all(),
            message='We already have an organization with this name'
        )],
    )
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
    organization_email = serializers.EmailField(max_length=128)

    def validate_github_url(self, value):
        """
        Check that the url provided is a valid github url
        """
        regex_pattern = "(https://)(www.)?(github.com/)([/A-Za-z0-9_-]+)"
        regex_result = re.search(regex_pattern, value)

        # if regex_result returns none it failed to match the entire string, raise error
        # or
        # if the lenght of the url is greater than the upper bound of the matched string, raise error
        if not regex_result or len(value) > regex_result.span()[1]:
            raise serializers.ValidationError("Not a valid GitHub URL")
        return value

    def validate_facebook_url(self, value):
        """
        Check that the value is a valid facebook  url
        """
        if not value.lower().startswith('https://www.facebook.com/'):
            raise serializers.ValidationError("Not a valid Facebook URL")
        return value

    def validate_twitter_url(self, value):
        """
        Check that the value is valid twitter url
        """
        if 'twitter.com/' not in value.lower():
            raise serializers.ValidationError("Not a valid Twitter URL")
        return value

    def validate_meetup_url(self, value):
        """
        Check that the value is a valid meetup url
        """
        if not value.lower().startswith('https://www.meetup.com/'):
            raise serializers.ValidationError("Not a valid meetup URL")
        return value

    def create(self):
        validated_data = self.validated_data
        links = [
            ('WebSite', validated_data.get('website_url')),
            ('GitHub', validated_data.get('github_url')),
            ('FaceBook', validated_data.get('facebook_url')),
            ('Twitter', validated_data.get('twitter_url')),
            ('MeetUp', validated_data.get('meetup_url')),
        ]

        org = Organization(
            name=validated_data["name"],
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            country=validated_data.get('country', ''),
            org_tag=validated_data['org_tag'],
            organization_email=validated_data['organization_email'],
        )
        if validated_data.get('parent_organization'):
            validated_data['parent_organization'].add_child(instance=org)
        else:
            Organization.get_first_root_node().add_child(instance=org)

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
