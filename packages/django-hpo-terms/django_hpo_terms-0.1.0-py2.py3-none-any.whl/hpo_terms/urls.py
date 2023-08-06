# -*- coding: utf-8 -*-
from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register(r'hpo-terms', viewsets.TermViewSet)
router.register(r'hpo-xrefs', viewsets.CrossReferenceViewSet)
router.register(r'diseases', viewsets.DiseaseViewSet)

default_router = routers.DefaultRouter()
default_router.register(r'hpo-terms', viewsets.TermViewSet)
default_router.register(r'hpo-xrefs', viewsets.CrossReferenceViewSet)
default_router.register(r'diseases', viewsets.DiseaseViewSet)


urlpatterns = default_router.urls
