# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


QUALIFIERS = Choices(
    (1, 'Bilateral', _('Bilateral')),
    (2, 'Chronic', _('Chronic')),
    (3, 'Distal', _('Distal')),
    (4, 'Episodic', _('Episodic')),
    (5, 'Generalized', _('Generalized')),
    (6, 'Mild', _('Mild')),
    (7, 'Moderate', _('Moderate')),
    (8, 'Non_Progressive', _('Non Progressive')),
    (9, 'Profound', _('Profound')),
    (10, 'Progressive', _('Progressive')),
    (11, 'Proximal', _('Proximal')),
    (12, 'Recurrent', _('Recurrent')),
    (13, 'Refractory', _('Refractory')),
    (14, 'Severe', _('Severe')),
)

CROSS_REFERENCES = Choices(
    (1, 'UMLS', _('UMLS')),
    (2, 'MSH', _('MSH')),
    (3, 'SNOMEDCT_US', _('SNOMEDCT_US')),
    (4, 'MEDDRA', _('MEDDRA')),
    (5, 'ICD-10', _('ICD-10')),
    (6, 'EPCC', _('EPCC')),
    (7, 'ICD-O', _('ICD-O')),
    (8, 'DOID', _('DOID')),
    (9, 'MP', _('MP')),
    (10, 'MPATH', _('MPATH')),
    (11, 'PMID', _('PMID')),
    (12, 'NCIT', _('NCIT')),
    (13, 'DOI', _('DOI')),
    (14, 'ORPHA', _('ORPHA')),
    (15, 'ICD-9', _('ICD-9')),
    (16, 'RGD', _('RGD')),
)

DATABASES = Choices(
    (1, 'OMIM', _('OMIM')),
    (2, 'ORPHA', _('ORPHA')),
    (3, 'DECIPHER', _('DECIPHER')),
)

EVIDENCE = Choices(
    (1, 'ICE', _('ICE')),
    (2, 'IEA', _('IEA')),
    (3, 'PCS', _('PCS')),
    (4, 'TAS', _('TAS')),
)

SYNONYM_SCOPES = Choices(
    (1, 'EXACT', _('EXACT')),
    (2, 'BROAD', _('BROAD')),
    (3, 'NARROW', _('NARROW')),
    (4, 'RELATED', _('RELATED')),
)
