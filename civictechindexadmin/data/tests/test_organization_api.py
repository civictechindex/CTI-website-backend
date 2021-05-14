import pytest
from django.urls import resolve
from django.utils.text import slugify

from ..models import Organization
from .factories import AliasFactory, LinkFactory, OrganizationFactory

pytestmark = pytest.mark.django_db


def test_get_organizations(api_client):
    approved_org = OrganizationFactory(name='Yup', status='approved')
    denied_org = OrganizationFactory(name='Nope', status='denied')  # noqa
    submitted_org = OrganizationFactory(name='Maybe', status='submitted')  # noqa
    url = '/api/organizations/'
    assert resolve(url).url_name == 'organization-list'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == approved_org.name
    assert not data[0]['affiliated']


def test_search_organizations(api_client):
    hack = OrganizationFactory(name='Hack for Austin')
    open_org = OrganizationFactory(name='Open Austin', city='Austin', state='Texas')
    open_other = OrganizationFactory(name='Open Houston', city='Houston', state='Texas')
    response = api_client.get('/api/organizations/?search=Austin')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert hack.name in [o['name'] for o in data]
    assert open_org.name in [o['name'] for o in data]
    # Now search for Texas
    response = api_client.get('/api/organizations/?search=Texas')
    assert [open_org.name, open_other.name] == [o['name'] for o in response.json()]


def _get_org_detail_page(api_client, org):
    """Helper method to dry up repeated calls to org detail page"""
    url = f'/api/organizations/{org.slug}/'
    response = api_client.get(url)
    assert response.status_code == 200
    return response.json()


def test_get_organization_detail(api_client):
    org = OrganizationFactory()
    data = _get_org_detail_page(api_client, org)
    assert data['name'] == org.name
    assert data['slug'] == slugify(org.name)
    assert not data['affiliated']


def test_get_org_detail_does_not_show_submitted(api_client):
    org = OrganizationFactory(status='submitted')
    url = f'/api/organizations/{org.slug}/'
    response = api_client.get(url)
    assert response.status_code == 404


def test_get_org_detail_does_not_show_denied(api_client):
    org = OrganizationFactory(name='Evil', status='denied')
    url = f'/api/organizations/{org.slug}/'
    response = api_client.get(url)
    assert response.status_code == 404
    assert response.json()['detail'] == "No organization by the name of 'evil'"


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
    data = _get_org_detail_page(api_client, org)
    assert data['name'] == org.name
    assert len(data['links']) == 2
    assert link1.url in [link['url'] for link in data['links']]
    assert link2.url in [link['url'] for link in data['links']]


def test_get_organization_detail_includes_aliases(api_client):
    org = OrganizationFactory(org_tag='code-for-somewhere')
    AliasFactory(tag='code-for-somewhere', alias='code4somewhere')
    AliasFactory(tag='code-for-somewhere', alias='codeforsomewhere')
    data = _get_org_detail_page(api_client, org)
    assert data['name'] == org.name
    assert data['org_tag'] == org.org_tag
    assert sorted(data['aliases']) == ['code4somewhere', 'codeforsomewhere']


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
        'github_url': 'https://github.com/hackforla',
        'org_tag': 'hack4pasadena',
    }


def _check_response(response, input_data):
    assert response['name'] == input_data['name']
    assert response['city'] == input_data['city']
    assert response['state'] == input_data['state']
    assert response['country'] == input_data['country']
    assert response['org_tag'] == input_data['org_tag']
    assert input_data['github_url'] in [link['url'] for link in response['links']]


def test_create_organization_with_sparse_input(api_client):
    # we need to create a root (even if we don't pass it in the request)
    root = Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = {
        'name': 'Code for Berwick',
        'organization_email': 'cfp@example.org',
        'github_url': 'https://www.github.com/hackforla',
        'org_tag': 'hack4berwick',
    }

    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Code for Berwick'
    assert data['slug'] == 'code-for-berwick'
    assert data['depth'] == 2
    assert data['path'][:-4] == root.path
    assert data['city'] == ''


def test_create_organization_with_all_values(api_client):
    # we need to create a root (even if we don't pass it in the request)
    root = Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['facebook_url'] = 'https://www.facebook.com/hackforla'
    input_data['meetup_url'] = 'https://www.meetup.com/hackforla'
    input_data['twitter_url'] = 'https://twitter.com/hackforla'
    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    _check_response(data, input_data)
    # With no explicit parent, this is added below root
    assert data['depth'] == 2
    assert data['path'][:-4] == root.path
    assert len(data['links']) == 4
    # Organizations without parents are not "affilited"
    assert not data['affiliated']


def test_create_organization_with_parent(api_client):
    parent_org = OrganizationFactory.create(name='Code for All', github_id=12345)
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['parent_organization'] = parent_org.id

    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    _check_response(data, input_data)
    assert data['depth'] == 3
    assert data['path'][:-4] == parent_org.path
    # Organizations with parents are "affilited"
    assert data['affiliated']


def test_organization_created_with_status_submitted(api_client):
    """
    This test checks the fields that are created when posting to
    AddOrganizationSerializer but are not returned in the JSON response.
    """
    # we need to creat a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()
    response = api_client.post(url, input_data)
    assert response.status_code == 201
    data = response.json()
    new_org = Organization.objects.get(pk=data['id'])
    assert new_org.status == 'submitted'
    assert new_org.organization_email == input_data['organization_email']


def test_create_duplicate_org_errors_gracefully(api_client):
    # we need to create a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()

    # First submit is fine
    response = api_client.post(url, input_data)
    assert response.status_code == 201

    # Duplicate submit gives 'invalid input' error
    response = api_client.post(url, input_data)
    assert response.status_code == 400
    assert response.json()['name'] == ['We already have an organization with this name']


def test_create_organization_with_invalid_github_url(api_client):
    """
    This check tests that request with an incorrectly formatted
    github url returns a status code of 400
    """
    # we need to create a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = {
        'name': 'Code for Berwick',
        'organization_email': 'cfp@example.org',
        'github_url': 'https://hackforla.org',
        'org_tag': 'hack4berwick',
    }

    response = api_client.post(url, input_data)
    data = response.json()
    assert response.status_code == 400
    assert data['github_url'] == ['Not a valid GitHub URL']


def test_create_organization_with_invalid_meetup_url(api_client):
    """
    This check tests that request with an incorrectly formatted
    meetup url returns a status code of 400
    """
    # we need to create a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['meetup_url'] = 'https://www.cat.org'

    response = api_client.post(url, input_data)
    data = response.json()
    assert response.status_code == 400
    assert data['meetup_url'] == ['Not a valid meetup URL']


def test_create_organization_with_invalid_facebook_url(api_client):
    """
    This check tests that request with an incorrectly formatted
    facebook url returns a status code of 400
    """
    # we need to create a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['facebook_url'] = 'https://www.cat.org'

    response = api_client.post(url, input_data)
    data = response.json()
    assert response.status_code == 400
    assert data['facebook_url'] == ['Not a valid Facebook URL']


def test_create_organization_with_invalid_twitter_url(api_client):
    """
    This check tests that request with an incorrectly formatted
    twitter url returns a status code of 400
    """
    # we need to create a root (even if we don't pass it in the request)
    Organization.add_root(name='Root')
    url = '/api/organizations/'
    input_data = _creation_data()
    input_data['twitter_url'] = 'https://www.cat.org'

    response = api_client.post(url, input_data)
    data = response.json()
    assert response.status_code == 400
    assert data['twitter_url'] == ['Not a valid Twitter URL']
