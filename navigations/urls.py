from django.urls import path, re_path

from .views import index

urlpatterns = [
    re_path(r'(?P<pk>\d*)', index)
]