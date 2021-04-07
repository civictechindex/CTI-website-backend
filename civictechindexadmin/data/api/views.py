from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ViewSet

from .serializers import (
    AddOrganizationSerializer, AliasSerializer, OrganizationSerializer, OrganizationFullSerializer,
    FAQSerializer, LinkSerializer, NotificationSubscriptionSerializer,
)
from ..models import Organization, Link, FAQ, Alias


class OrganizationViewSet(ViewSet):
    @swagger_auto_schema(responses={200: OrganizationSerializer(many=True)})
    def list(self, request):
        queryset = Organization.objects.all()
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: OrganizationFullSerializer()})
    def retrieve(self, request, pk=None):
        org = Organization.objects.filter(name=pk).prefetch_related('links').first()
        if not org:
            raise NotFound(f"No organization by the name of '{pk}'")
        serializer = OrganizationFullSerializer(org)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: OrganizationFullSerializer()})
    def create(self, request):
        serializer = AddOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            new_org = serializer.create()
            return Response(OrganizationFullSerializer(new_org).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: OrganizationFullSerializer()})
@api_view(['GET'])
def org_by_github_id(request, github_id):
    try:
        org = Organization.objects.get(github_id=github_id)
    except Organization.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OrganizationFullSerializer(org)
    return Response(serializer.data)


class LinkViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class MediumResultsSetPagination(PageNumberPagination):
    """
    Helper class for pagination settings.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class FAQViewSet(ReadOnlyModelViewSet):
    """
    FAQ's are managed via the Django admin interface. The API provides a list
    of live FAQ's in the order of most viewed. This viewset also provides an
    endpoint for tracking when a user clicks on the question to view the answer.
    """
    serializer_class = FAQSerializer
    queryset = FAQ.objects.filter(live=True).all().order_by('-view_count', 'question')
    filter_backends = [SearchFilter]
    search_fields = ['@question', '@answer']
    pagination_class = MediumResultsSetPagination

    @action(detail=True, methods=['post'])
    def increment_count(self, request, pk=None):
        faq = FAQ.objects.filter(pk=pk).first()
        if faq:
            try:
                FAQ.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

            return Response("", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(f"FAQ {pk} not found", status=status.HTTP_404_NOT_FOUND)


class AliasViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = AliasSerializer
    queryset = Alias.objects.all()
    lookup_field = "alias"


@swagger_auto_schema(method='post', request_body=NotificationSubscriptionSerializer)
@api_view(['POST'])
def subscribe(request):
    """
    At least at the moment, we only want to create NotificationSubscriptions.
    The only people who should have access to see the collected information
    can see (and manage) it from the django admin interface.
    """
    serializer = NotificationSubscriptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(ip_address=request.META["REMOTE_ADDR"])
    return Response(serializer.data, status=status.HTTP_201_CREATED)
