import pytest
from django.urls import reverse, resolve

from .factories import FAQFactory


pytestmark = pytest.mark.django_db


def test_get_api_faqs(api_client):
    url = '/api/faqs/'
    assert resolve(url).url_name == 'faq-list'
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_api_faqs_detail(api_client):
    faq = FAQFactory(live=True)
    url = f'/api/faqs/{faq.id}/'
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_api_faqs_detail_not_found_if_not_live(api_client):
    faq = FAQFactory(live=False)
    url = f'/api/faqs/{faq.id}/'
    response = api_client.get(url)
    assert response.status_code == 404


def test_post_api_faqs_method_not_allowed(api_client):
    url = '/api/faqs/'
    response = api_client.post(url, data={})
    assert response.status_code == 405


def test_post_api_faqs_detail_method_not_allowed(api_client):
    faq = FAQFactory(live=True)
    url = f'/api/faqs/{faq.id}/'
    response = api_client.post(url, data={})
    assert response.status_code == 405


def test_increment_faq_view_count(api_client):
    faq = FAQFactory(live=True)
    assert faq.view_count == 0
    response = api_client.post(reverse('api:faq-increment-count', kwargs={'pk': faq.id}), data={})
    assert response.status_code == 204
    faq.refresh_from_db()
    assert faq.view_count == 1


def test_increment_faq_view_count_when_faq_not_found(api_client):
    response = api_client.post(reverse('api:faq-increment-count', kwargs={'pk': 9999}), data={})
    assert response.status_code == 404
