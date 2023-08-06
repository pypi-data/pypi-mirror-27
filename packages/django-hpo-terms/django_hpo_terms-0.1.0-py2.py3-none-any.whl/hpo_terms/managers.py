# -*- coding: utf-8 -*-
from django.db import models


class TermQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('version').prefetch_related('is_a').all()


class CrossReferenceQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('hpo_term').all()


class DiseaseQuerySet(models.QuerySet):

    def fast(self):
        return self.select_related('mode_of_inheritance').prefetch_related('hpo_terms').all()
