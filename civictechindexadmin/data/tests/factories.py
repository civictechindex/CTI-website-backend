from django.conf import settings
from factory import DjangoModelFactory, Iterator, Sequence, SubFactory

from ..models import FAQ, Link, Organization


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = Sequence(lambda n: "user_%d" % n)


class FAQFactory(DjangoModelFactory):
    class Meta:
        model = FAQ
        django_get_or_create = ["question"]

    question = Sequence(lambda n: "Question %d" % n)
    answer = Sequence(lambda n: "Answer %d" % n)
    created_by = SubFactory(UserFactory)
    modified_by = created_by


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ["name"]

    name = Sequence(lambda n: "Open Thing %d" % n)
    # This is most useful if we get usable Organizations by default
    status = 'approved'


# NOTE to use this you must instantiate with he related Organization
class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link
        django_get_or_create = ["url"]

    link_type = Iterator(['WebSite', 'MeetUp', 'FaceBook', 'Twitter', 'GitHub'])
    url = Sequence(lambda n: "https://example.com/%d" % n)
