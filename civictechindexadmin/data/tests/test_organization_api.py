import pytest
from django.urls import resolve

from .factories import LinkFactory, OrganizationFactory


pytestmark = pytest.mark.django_db


def test_get_organizations(api_client):
    url = '/api/organizations/'
    assert resolve(url).url_name == 'organization-list'
    response = api_client.get(url)
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) == 0


def test_get_organization_detail(api_client):
    org = OrganizationFactory()
    url = f'/api/organizations/{org.name}/'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == org.name


def test_get_organization_detail_includes_links(api_client):
    org = OrganizationFactory()
    link1 = LinkFactory(organization=org)
    link2 = LinkFactory(organization=org)
    url = f'/api/organizations/{org.name}/'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == org.name
    assert len(data['links']) == 2
    assert link1.url in [link['url'] for link in data['links']]
    assert link2.url in [link['url'] for link in data['links']]
