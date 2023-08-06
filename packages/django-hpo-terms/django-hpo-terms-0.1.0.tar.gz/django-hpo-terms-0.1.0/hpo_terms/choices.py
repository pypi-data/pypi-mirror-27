from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


QUALIFIERS = Choices(
    (1, 'BILATERAL', _('Bilateral')),
    (2, 'CHRONIC', _('Chronic')),
    (3, 'DISTAL', _('Distal')),
    (4, 'EPISODIC', _('Episodic')),
    (5, 'GENERALIZED', _('Generalized')),
    (6, 'MILD', _('Mild')),
    (7, 'MODERATE', _('Moderate')),
    (8, 'NONPROGRESSIVE', _('Non Progressive')),
    (9, 'PROFOUND', _('Profound')),
    (10, 'PROGRESSIVE', _('Progressive')),
    (11, 'PROXIMAL', _('Proximal')),
    (12, 'RECURRENT', _('Recurrent')),
    (13, 'REFRACTORY', _('Refractory')),
    (14, 'SEVERE', _('Severe')),
    (999, 'NA', _('Mixed')),
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
    (1, 'E', _('EXACT')),
    (2, 'B', _('BROAD')),
    (3, 'N', _('NARROW')),
    (4, 'R', _('RELATED')),
)
