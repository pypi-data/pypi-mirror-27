from django.conf import settings

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework_jwt.settings import api_settings

from .. import factories


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class APITestCase(BaseAPITestCase):
    VERSION = 'v1'

    def setUp(self):
        self.password = 'test'
        self.user = factories.UserFactory(password=self.password)
        self.factory = APIRequestFactory()

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

        self.client.credentials(
            HTTP_AUTHORIZATION='{prefix} {token}'.format(
                prefix=api_settings.JWT_AUTH_HEADER_PREFIX,
                token=self.token),
            HTTP_ACCEPT='application/vnd.{0}.{1}+json'
            .format(settings.SITE_NAME, self.VERSION),
            HTTP_CONTENT_TYPE='application/json')
