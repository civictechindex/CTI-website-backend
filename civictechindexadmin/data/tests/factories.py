from django.conf import settings
from factory import DjangoModelFactory, Iterator, Sequence, SubFactory

from ..models import Alias, FAQ, Link2, Organization2


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
        model = Organization2
        django_get_or_create = ["name"]

    name = Sequence(lambda n: "Open Thing %d" % n)
    # This is most useful if we get usable Organizations by default
    status = 'approved'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create``to incorporate add_child."""
        if 'parent' in kwargs.values():
            parent = kwargs['parent']
        elif model_class.get_first_root_node():
            parent = model_class.get_first_root_node()
        else:
            parent = model_class.add_root(name='Root')
        obj = model_class(**kwargs)
        return parent.add_child(instance=obj)


# NOTE to use this you must instantiate with the related Organization
class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link2
        django_get_or_create = ["url"]

    link_type = Iterator(['WebSite', 'MeetUp', 'FaceBook', 'Twitter', 'GitHub'])
    url = Sequence(lambda n: "https://example.com/%d" % n)


class AliasFactory(DjangoModelFactory):
    class Meta:
        model = Alias

    tag = Sequence(lambda n: "tag_%d" % n)
    alias = Sequence(lambda n: "alias_%d" % n)
