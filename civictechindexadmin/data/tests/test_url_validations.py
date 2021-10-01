import pytest
from rest_framework.serializers import ValidationError
from civictechindexadmin.data.api.serializers import AddOrganizationSerializer


good_github_urls = [
    # 'http://www.github.com/person/repository',
    # 'http://github.com/person/repository',
    'https://www.github.com/person/repository',
    'https://github.com/person/repository',
]


@pytest.mark.parametrize("test_url", good_github_urls)
def test_github_url_validation_good_urls(test_url):
    assert test_url == AddOrganizationSerializer().validate_github_url(test_url)


bad_github_urls = [
    'http://github.com/',
]


@pytest.mark.parametrize("test_url", bad_github_urls)
def test_github_url_validation__urls(test_url):
    with pytest.raises(ValidationError) as e_info:
        AddOrganizationSerializer().validate_github_url(test_url)
        assert e_info == "Not a valid GitHub URL"
