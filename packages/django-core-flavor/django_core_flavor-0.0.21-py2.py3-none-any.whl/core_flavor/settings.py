import environ


env = environ.Env()

CORE_REQUEST_LOGGER_NAME = env(
    'CORE_REQUEST_LOGGER_NAME',
    default='django.request')
