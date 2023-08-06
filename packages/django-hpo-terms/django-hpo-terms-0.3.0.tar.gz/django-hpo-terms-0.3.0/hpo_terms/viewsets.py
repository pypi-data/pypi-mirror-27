# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from genome.models import Gene
from genome.filters import GeneFilter
from genome.serializers import GeneSerializer

from . import filters, models, serializers


class TermViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing HPO Terms."""

    queryset = models.Term.objects.fast()
    serializer_class = serializers.TermSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = filters.TermFilter
    search_fields = (
        'label',
        'description',
        'synonyms__description',
    )


class CrossReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing HPO Term Cross References."""

    queryset = models.CrossReference.objects.fast()
    serializer_class = serializers.CrossReferenceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = filters.CrossReferenceFilter
    search_fields = (
        'hpo_term__label',
        'hpo_term__description',
        'hpo_term__synonyms__description',
        'hpo_term__diseases__description',
        'source_value',
    )


class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Diseases."""

    queryset = models.Disease.objects.fast()
    serializer_class = serializers.DiseaseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = filters.DiseaseFilter
    search_fields = (
        'description',
        'hpo_terms__label',
        'hpo_terms__description',
        'hpo_terms__synonyms__description',
    )


class DiseaseGeneViewSet(viewsets.ReadOnlyModelViewSet):
    """A simple ViewSet for viewing Disease Genes."""

    queryset = Gene.objects.prefetch_related('diseases__hpo_terms').filter(diseases__id__isnull=False)
    serializer_class = GeneSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = GeneFilter
    search_fields = (
        'diseases__description',
        'diseases__hpo_terms__label',
        'diseases___hpo_terms__description',
        'diseases___hpo_terms__synonyms__description',
    )
