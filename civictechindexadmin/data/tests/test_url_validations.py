import pytest
from rest_framework.serializers import ValidationError
from civictechindexadmin.data.api.serializers import AddOrganizationSerializer


good_github_urls = [
    'https://www.github.com/person/repository',
    'https://github.com/person/repository',
    'http://www.github.com/person/repository',
    'http://github.com/person/repository',
    'www.github.com/person/repository',
    'github.com/person/repository',
    'github.com/per-son/repo-si.to_ry2020',
    'https://github.com/civictechindex',
    'https://github.com/civictechindex/CTI-website-backend'
]

@pytest.mark.parametrize("test_url", good_github_urls)
def test_github_url_validation_good_urls(test_url):
    assert test_url == AddOrganizationSerializer().validate_github_url(test_url)


bad_github_urls = [
    'github.com/',
    'bad://github.com/person/repository',
    'bad.github.com/person/repository',
]

@pytest.mark.parametrize("test_url", bad_github_urls)
def test_github_url_validation__urls(test_url):
    with pytest.raises(ValidationError) as e_info:
        AddOrganizationSerializer().validate_github_url(test_url)
        assert e_info == "Not a valid GitHub URL"


good_facebook_urls = [
    'https://www.facebook.com/person',
    'https://facebook.com/person',
    'http://www.facebook.com/person',
    'http://facebook.com/person',
    'www.facebook.com/person',
    'facebook.com/person',
    'facebook.com/perso',
    'facebook.com/pe.rso2020',
]

@pytest.mark.parametrize("test_url", good_facebook_urls)
def test_facebook_url_validation_good_urls(test_url):
    assert test_url == AddOrganizationSerializer().validate_facebook_url(test_url)


bad_facebook_urls = [
    'facebook.com/',
    'bad://facebook.com/person',
    'bad.facebook.com/person',
    'facebook.com/pers',
    #'facebook.com/pe.rs',
]

@pytest.mark.parametrize("test_url", bad_facebook_urls)
def test_facebook_url_validation__urls(test_url):
    with pytest.raises(ValidationError) as e_info:
        AddOrganizationSerializer().validate_facebook_url(test_url)
        assert e_info == "Not a valid Facebook URL"


good_twitter_urls = [
    'https://www.twitter.com/person',
    'https://twitter.com/person',
    'http://www.twitter.com/person',
    'http://twitter.com/person',
    'www.twitter.com/person',
    'twitter.com/person',
    'twitter.com/perso',
    'twitter.com/pe_rso2020',
]

@pytest.mark.parametrize("test_url", good_twitter_urls)
def test_twitter_url_validation_good_urls(test_url):
    assert test_url == AddOrganizationSerializer().validate_twitter_url(test_url)


bad_twitter_urls = [
    'twitter.com/',
    'bad://twitter.com/person',
    'bad.twitter.com/person',
    'twitter.com/pers',
    'twitter.com/pe#rson',
]

@pytest.mark.parametrize("test_url", bad_twitter_urls)
def test_twitter_url_validation__urls(test_url):
    with pytest.raises(ValidationError) as e_info:
        AddOrganizationSerializer().validate_meetup_url(test_url)
        assert e_info == "Not a valid Facebook URL"


good_meetup_urls = [
    'https://www.meetup.com/person',
    'https://meetup.com/person',
    'http://www.meetup.com/person',
    'http://meetup.com/person',
    'www.meetup.com/person',
    'meetup.com/person',
    'meetup.com/per-son2020',
]

@pytest.mark.parametrize("test_url", good_meetup_urls)
def test_meetup_url_validation_good_urls(test_url):
    assert test_url == AddOrganizationSerializer().validate_meetup_url(test_url)


bad_meetup_urls = [
    'meetup.com/',
    'bad://meetup.com/person',
    'bad.meetup.com/person',
    'meetup.com/perso',
    'meetup.com/pe.rso',
]

@pytest.mark.parametrize("test_url", bad_meetup_urls)
def test_meetup_url_validation__urls(test_url):
    with pytest.raises(ValidationError) as e_info:
        AddOrganizationSerializer().validate_meetup_url(test_url)
        assert e_info == "Not a valid Facebook URL"
