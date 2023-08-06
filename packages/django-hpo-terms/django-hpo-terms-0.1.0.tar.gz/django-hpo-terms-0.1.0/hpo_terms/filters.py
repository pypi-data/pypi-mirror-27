# -*- coding: utf-8 -*-
from django.db.models import Q

import django_filters

from . import models, utils


class TermFilter(django_filters.rest_framework.FilterSet):

    hpo_term = django_filters.CharFilter(
        method='filter_hpo_term',
        label='HPO Term',
    )

    is_a = django_filters.CharFilter(
        method='filter_is_a',
        label='Is a',
    )

    can_be = django_filters.CharFilter(
        method='filter_can_be',
        label='Can be',
    )

    class Meta:
        model = models.Term
        fields = [
            'version',
            'identifier',
            'label',
            'description',
        ]

    def filter_hpo_term(self, queryset, name, value):
        return queryset.filter(Q(identifier=utils.normalize_hpo_id(value)))

    def filter_is_a(self, queryset, name, value):
        return queryset.filter(Q(is_a__identifier=utils.normalize_hpo_id(value)))

    def filter_can_be(self, queryset, name, value):
        return queryset.filter(Q(can_be__identifier=utils.normalize_hpo_id(value)))


class CrossReferenceFilter(django_filters.rest_framework.FilterSet):

    hpo_term = django_filters.CharFilter(
        method='filter_hpo_term',
        label='HPO Term',
    )

    class Meta:
        model = models.CrossReference
        fields = [
            'source',
            'source_value',
        ]

    def filter_hpo_term(self, queryset, name, value):
        return queryset.filter(Q(hpo_term__identifier=utils.normalize_hpo_id(value)))


class DiseaseFilter(django_filters.rest_framework.FilterSet):

    hpo_term = django_filters.CharFilter(
        method='filter_hpo_term',
        label='HPO Term',
    )

    mode_of_inheritance = django_filters.CharFilter(
        method='filter_mode_of_inheritance',
        label='Mode of Inheritance',
    )

    age_of_onset = django_filters.CharFilter(
        method='filter_age_of_onset',
        label='Age of Onset',
    )

    frequency = django_filters.CharFilter(
        method='filter_frequency',
        label='Frequency',
    )

    class Meta:
        model = models.Disease
        fields = [
            'database',
            'identifier',
            'description',
            'qualifier',
            'evidence_code',
        ]

    def filter_hpo_term(self, queryset, name, value):
        return queryset.filter(Q(hpo_terms__identifier=utils.normalize_hpo_id(value)))

    def filter_mode_of_inheritance(self, queryset, name, value):
        return queryset.filter(Q(mode_of_inheritance__identifier=utils.normalize_hpo_id(value)))

    def filter_age_of_onset(self, queryset, name, value):
        return queryset.filter(Q(age_of_onset__identifier=utils.normalize_hpo_id(value)))

    def filter_frequency(self, queryset, name, value):
        return queryset.filter(Q(frequency__identifier=utils.normalize_hpo_id(value)))
