import logging

try:
    import urllib2 as urllib
except ImportError:
    from urllib import request as urllib

import pronto

from django.core.exceptions import ObjectDoesNotExist

from . import choices, models


logger = logging.getLogger(__name__)


def normalize_hpo_id(hpo_term):
    """Reformat HPO Term to database Id

    Arguments:
        hpo_term (str): HPO Term

    Returns:
        int: HPO database Id
    """
    if hpo_term.startswith('HP:'):
        hpo_id = hpo_term.lstrip('HP:')
    else:
        hpo_id = hpo_term

    return int(hpo_id.lstrip('0'))


def sync_from_hpo():
    """Syncs HPO terms from HPO Team"""
    from .app_settings import HPO_URL, HPO_PHENOTYPES_URL

    logger.info('Syncing from HPO')

    hpo = pronto.Ontology(HPO_URL, timeout=10)

    # Create Version object
    version_obj, version_created = models.Version.objects.get_or_create(
        # NOTE: pronto always returns array
        label=hpo.meta['data-version'][0]
    )

    # If new version, then we need to sync HPO terms
    if version_created:

        logger.info('Syncing new version: {0}'.format(hpo.meta['data-version'][0]))
        # Create Term objects
        for term in hpo:

            identifier = normalize_hpo_id(term.id)
            label = term.name
            description = term.desc
            created_by = term.other.get('created_by')
            created = term.other.get('creation_date')

            alternate_ids = [
                str(normalize_hpo_id(alt_term))
                for alt_term in term.other.get('alt_id', [])
            ]

            try:
                term_obj = models.Term.objects.create(
                    version=version_obj,
                    identifier=identifier,
                    label=label if label else "",
                    description=description if description else "",
                    created_by=created_by if created_by else "",
                    created=created[0] if created else "",
                    alternate_ids=",".join(alternate_ids),
                )
            except Exception as error:
                raise Exception('HPO: {0} could not be added! Error: {1}'.format(term.id, error))

            # Create Synonym objects
            for synonym in term.synonyms:
                if synonym:

                    synonym_obj, synonym_created = models.Synonym.objects.get_or_create(
                        hpo_term=term_obj,
                        description=synonym.desc if synonym.desc else "",
                        # NOTE: pronto always returns array
                        scope=getattr(choices.SYNONYM_SCOPES, str(synonym.scope)[0]),
                    )

            # Create CrossReference objects
            for xref in term.other.get('xref', []):
                if xref:
                    xref_data = xref.split(':', 1)

                    # NOTE: We want source and id to store. There are 3 records that don't conform
                    if len(xref_data) != 2 or xref_data[0].upper() == 'HTTP':
                        err_msg = 'Format of XRef: {0} for {1} is not supported!'.format(xref, term.id)
                        logger.info(err_msg)
                        continue

                    xref_obj, xref_created = models.CrossReference.objects.get_or_create(
                        hpo_term=term_obj,
                        # NOTE: pronto always returns array
                        source=getattr(choices.CROSS_REFERENCES, str(xref_data[0].upper())),
                        source_value=xref_data[1],
                    )

        # Create Disease objects
        logger.info('Syncing Phenotypes from HPO')
        for line in urllib.urlopen(HPO_PHENOTYPES_URL).read().decode('utf-8').strip().split('\n'):
            disease_record = line.strip().split('\t')

            # NOTE: some OMIM records are screwed up, we skip those
            try:
                identifier = int(disease_record[1])
            except ValueError:
                logger.info('Skipping: {0}'.format(disease_record))
                continue

            database = getattr(choices.DATABASES, disease_record[0])

            description = disease_record[2]
            qualifier = getattr(choices.DATABASES, disease_record[3], None)
            evidence_code = getattr(choices.DATABASES, disease_record[6], None)
            age_of_onset = disease_record[7].strip()
            frequency = disease_record[8].strip()
            create_date = disease_record[12]
            assigned_by = disease_record[13]

            if age_of_onset:
                try:
                    age_of_onset_obj = models.Term.objects.get(identifier=normalize_hpo_id(age_of_onset))
                except ObjectDoesNotExist:
                    age_of_onset_obj = None
            else:
                age_of_onset_obj = None

            if frequency:
                try:
                    frequency_obj = models.Term.objects.get(identifier=normalize_hpo_id(frequency))
                except ObjectDoesNotExist:
                    frequency_obj = None
            else:
                frequency_obj = None

            disease_obj, updated = models.Disease.objects.update_or_create(
                version=version_obj,
                database=database,
                identifier=identifier,
                defaults={
                    'description': description,
                    'qualifier': qualifier,
                    'evidence_code': evidence_code,
                    'age_of_onset': age_of_onset_obj,
                    'frequency': frequency_obj,
                    'create_date': create_date,
                    'assigned_by': assigned_by,
                }
            )

            hpo_term = models.Term.objects.get(
                identifier=normalize_hpo_id(disease_record[4])
            )

            disease_obj.hpo_terms.add(hpo_term)
            disease_obj.save()
