import re

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse_lazy
from rest_framework.validators import UniqueValidator

from ..models import Organization, Link, FAQ, NotificationSubscription, Alias


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'link_type', 'url']
        depth = 1


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    affiliated = serializers.SerializerMethodField()
    links = LinkSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'depth', 'path', 'name', 'slug', 'url', 'github_name', 'github_id',
                  'cti_contributor', 'city', 'state', 'country', 'image_url', 'org_tag',
                  'affiliated', 'links', ]

    def get_affiliated(self, org):
        return not (org.depth == 2 and org.numchild == 0)

    def get_url(self, org):
        request = self.context['request']
        return reverse_lazy('api:organization-detail', args=[org.slug], request=request)


class OrganizationFullSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)
    aliases = serializers.SerializerMethodField()
    affiliated = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'depth', 'path', 'name', 'slug', 'github_name', 'github_id',
                  'cti_contributor', 'city', 'state', 'country', 'image_url', 'org_tag',
                  'links', 'aliases', 'affiliated', 'parents', 'children', ]

    def get_aliases(self, org):
        return [a.alias for a in Alias.objects.filter(tag=org.org_tag).all()]

    def get_affiliated(self, org):
        return not (org.depth == 2 and org.numchild == 0)

    def get_parents(self, org):
        parents = org.get_ancestors()
        return [{'slug': n.slug, 'name': n.name, 'org_tag': n.org_tag} for n in parents if n.depth > 1]

    def get_children(self, org):
        children = org.get_descendants()
        return [{'slug': n.slug, 'name': n.name, 'org_tag': n.org_tag} for n in children if n.depth > 1]


def addURLPrefix(value):
    if not value.lower().startswith('https://') and not 'https://' in value.lower() and not 'http://' in value.lower():
        value = 'https://' + value
    return value

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
        regex_pattern = "^(?:http(?:|s)://)?(?:www.)?github.com/(?:[/a-z0-9_.-]+)$"
        regex_result = re.search(regex_pattern, value.lower())

        if not regex_result:
            raise serializers.ValidationError("Not a valid GitHub URL")
        return addURLPrefix(value)

    def validate_facebook_url(self, value):
        """
        Check that the value is a valid facebook url
        """
        regex_pattern = "^(?:http(?:|s)://)?(?:www.)?facebook.com/(?:[a-z0-9]|.(?=[a-z0-9])){5,}$"
        regex_result = re.search(regex_pattern, value.lower())

        if not regex_result:
            raise serializers.ValidationError("Not a valid Facebook URL")
        return addURLPrefix(value)

    def validate_twitter_url(self, value):
        """
        Check that the value is valid twitter url
        """
        regex_pattern = "^(?:http(?:|s)://)?(?:www.)?twitter.com/(?:[a-z0-9_]{5,15})$"
        regex_result = re.search(regex_pattern, value.lower())

        if not regex_result:
            raise serializers.ValidationError("Not a valid Twitter URL")
        return addURLPrefix(value)

    def validate_meetup_url(self, value):
        """
        Check that the value is a valid meetup url
        """
        regex_pattern = "^(?:http(?:|s)://)?(?:www.)?meetup.com/(?:[a-z0-9-]{6,70})$"
        regex_result = re.search(regex_pattern, value.lower())

        if not regex_result:
            raise serializers.ValidationError("Not a valid meetup URL")
        return addURLPrefix(value)

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
