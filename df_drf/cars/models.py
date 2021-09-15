# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'nombre')
    created = models.DateTimeField(verbose_name=u'fecha creación')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'creado en')

    @property
    def num_of_cars(self):
        return Car.objects.filter(brand=self).count()

    class Meta:
        ordering = ['name']
        verbose_name = u'Marca'
        verbose_name_plural = u'Marcas'

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'nombre')
    height = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=u'altura')
    width = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=u'ancho')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=u'marca')

    class Meta:
        ordering = ['name']
        verbose_name = u'coche'
        verbose_name_plural = u'coches'

    def __str__(self):
        return f'{brand.name} - {self.name}'
