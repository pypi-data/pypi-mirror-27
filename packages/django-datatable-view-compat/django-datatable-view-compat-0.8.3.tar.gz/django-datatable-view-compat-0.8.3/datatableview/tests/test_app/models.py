# -*- encoding: utf-8 -*-

from django.db import models


class ExampleModel(models.Model):
    name = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)
    related = models.ForeignKey('RelatedModel', models.CASCADE, blank=True, null=True)
    relateds = models.ManyToManyField('RelatedM2MModel', blank=True)

    def __str__(self):
        return 'ExampleModel object'

    def get_absolute_url(self):
        return "#{pk}".format(pk=self.pk)


class RelatedModel(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return 'RelatedModel object'

    def get_absolute_url(self):
        return "#{pk}".format(pk=self.pk)


class RelatedM2MModel(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return 'RelatedM2MModel object'


class ReverseRelatedModel(models.Model):
    name = models.CharField(max_length=15)
    example = models.ForeignKey('ExampleModel', models.CASCADE)

    def __str__(self):
        return 'ReverseRelatedModel object'
