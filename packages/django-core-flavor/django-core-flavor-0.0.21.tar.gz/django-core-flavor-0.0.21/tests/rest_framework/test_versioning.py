import re

from django.conf import settings
from core_flavor.rest_framework import middleware
from core_flavor.rest_framework.test import APITestCase


class VersioningTests(APITestCase):
    X_MEDIA_TYPE_PATTERN = re.compile(
        r'^{}(?P<sandbox>.sandbox)?.(?P<version>v\d+);'
        r' format=(?P<format>\S+)'
        .format(settings.SITE_NAME))

    def get_media_type(self, response):
        return self.X_MEDIA_TYPE_PATTERN\
            .match(
                response.get(
                    middleware.VersioningMiddleware.X_MEDIA_TYPE
                )
            )\
            .groupdict()

    def test_versioning_url(self):
        version_url = 'v2'
        response = self.client.get('/{}/test'.format(version_url))
        media_type = self.get_media_type(response)['version']

        self.assertEqual(media_type, version_url)

    def test_media_type(self):
        response = self.client.get('/')
        media_type = self.get_media_type(response)['version']

        self.assertEqual(media_type, self.VERSION)

    def test_format(self):
        self.client._credentials['HTTP_ACCEPT'] =\
            self.client._credentials['HTTP_ACCEPT']\
            .replace('json', 'api')

        response = self.client.get('/')
        media_type = self.get_media_type(response)['format']

        self.assertEqual(media_type, 'api')
