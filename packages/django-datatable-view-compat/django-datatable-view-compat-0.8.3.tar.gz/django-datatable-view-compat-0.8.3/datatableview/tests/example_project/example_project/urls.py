# -*- encoding: utf-8 -*-

from django.conf.urls import include, url

urlpatterns = (
    url(r'^', include('example_project.example_app.urls')),
)
