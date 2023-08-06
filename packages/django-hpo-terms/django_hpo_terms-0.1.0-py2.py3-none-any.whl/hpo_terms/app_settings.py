from django.conf import settings


hpo_purl = 'http://purl.obolibrary.org/obo/hp.obo'
hpo_phenotypes = 'http://compbio.charite.de/jenkins/job/hpo.annotations/'
hpo_phenotypes += 'lastSuccessfulBuild/artifact/misc/phenotype_annotation.tab'

HPO_URL = getattr(settings, 'HPO_URL', hpo_purl)
HPO_PHENOTYPES_URL = getattr(settings, 'HPO_PHENOTYPES_URL', hpo_phenotypes)
