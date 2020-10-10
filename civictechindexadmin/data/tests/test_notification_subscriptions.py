import pytest

from ..models import NotificationSubscription

pytestmark = pytest.mark.django_db


def test_subscribe_successful(api_client):
    subscription_count = NotificationSubscription.objects.count()
    url = '/api/subscribe/'
    response = api_client.post(url, data={'email_address': 'me@example.com', 'notification_type': 'test'})
    assert response.status_code == 201
    assert sorted(response.data.keys()) == ['created_date', 'email_address', 'ip_address', 'notification_type']
    assert NotificationSubscription.objects.count() == subscription_count + 1


def test_subscribe_email_address_is_required(api_client):
    subscription_count = NotificationSubscription.objects.count()
    url = '/api/subscribe/'
    response = api_client.post(url, data={'notification_type': 'test'})
    assert response.status_code == 400
    assert list(response.data.keys()) == ['email_address']
    assert response.data['email_address'][0].code == 'required'
    assert NotificationSubscription.objects.count() == subscription_count


def test_subscribe_type_is_required(api_client):
    subscription_count = NotificationSubscription.objects.count()
    url = '/api/subscribe/'
    response = api_client.post(url, data={'email_address': 'me@example.com'})
    assert response.status_code == 400
    assert list(response.data.keys()) == ['notification_type']
    assert response.data['notification_type'][0].code == 'required'
    assert NotificationSubscription.objects.count() == subscription_count


def test_subscribe_will_not_accept_duplicates(api_client):
    subscription_count = NotificationSubscription.objects.count()
    url = '/api/subscribe/'
    first = api_client.post(url, data={'email_address': 'me@example.com', 'notification_type': 'test'})
    assert first.status_code == 201
    assert NotificationSubscription.objects.count() == subscription_count + 1
    second = api_client.post(url, data={'email_address': 'me@example.com', 'notification_type': 'test'})
    assert second.status_code == 400
    assert second.data[0].code == 'invalid'
    assert str(second.data[0]) == "We already have a subscription for me@example.com"
