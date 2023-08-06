from django.conf.urls import url
from rest_framework.views import APIView


app_name = 'tests.rest_framework.urls'

urlpatterns = [
    url(r'^test$', APIView.as_view(), name='test')
]
