from django.conf import settings
from factory import DjangoModelFactory, Sequence, SubFactory

from ..models import FAQ


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
