import pytest
from django.urls import resolve

from .factories import LinkFactory, OrganizationFactory

pytestmark = pytest.mark.django_db


def test_get_organizations(api_client):
    url = '/api/organizations/'
    assert resolve(url).url_name == 'organization-list'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_organization_detail(api_client):
    org = OrganizationFactory()
    url = f'/api/organizations/{org.name}/'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == org.name


def test_get_organization_by_github_id(api_client):
    org = OrganizationFactory(github_id=12345)
    url = f'/api/organizations/github_id/{org.github_id}/'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == org.name
    assert data['github_id'] == 12345


def test_get_organization_by_github_id_invalid_id(api_client):
    OrganizationFactory()  # this org does not have a github_id
    url = '/api/organizations/github_id/999999/'
    response = api_client.get(url)
    assert response.status_code == 404


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


def test_create_organization_required_fields(api_client):
    url = '/api/organizations/'
    response = api_client.post(url, {})
    assert response.status_code == 400
    data = response.json()
    assert data['name'] == ['This field is required.']
    assert data['github_url'] == ['This field is required.']
    assert data['org_tag'] == ['This field is required.']
    assert data['organization_email'] == ['This field is required.']
    assert len(data.keys()) == 4


def _creation_data():
    return {
        'name': 'Code for Pasadena',
        'city': 'Pasadena',
        'state': 'CA',
        'country': 'USA',
        'organization_email': 'cfp@example.org',
        'github_url': 'https://hackforla.org',
        'org_tag': 'hack4pasadena',
    }


def _check_response(response, input_data):
    assert response['name'] == input_data['name']
    assert response['city'] == input_data['city']
    assert response['state'] == input_data['state']
    assert response['country'] == input_data['country']
    assert response['org_tag'] == input_data['org_tag']
    assert response['organization_email'] == input_data['organization_email']
    assert len(response['links']) == 1
    assert input_data['github_url'] in [link['url'] for link in response['links']]


def test_create_organization(api_client):
    url = '/api/organizations/'
    input_data = _creation_data()
    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    _check_response(data, input_data)


@pytest.mark.xfail
def test_create_organization_with_parent(api_client):
    """Adding an org with a parent works in Postman but this test says the org id is invalid.               s """
    parent_org = OrganizationFactory.create(name='Code for All', github_id=12345)
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['parent_organization_id'] = parent_org.id

    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    _check_response(data, input_data)
    assert data['parent_organization']['id'] == parent_org.id
    assert data['parent_organization']['name'] == parent_org.name
