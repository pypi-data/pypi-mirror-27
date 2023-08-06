# -*- encoding: utf-8 -*-
from distutils.version import StrictVersion

from django import get_version, template

register = template.Library()

if StrictVersion(get_version()) < StrictVersion('1.5'):
    from django.core.urlresolvers import reverse

    @register.simple_tag(name="url")
    def django_1_4_url_simple(url_name):
        return reverse(url_name)
