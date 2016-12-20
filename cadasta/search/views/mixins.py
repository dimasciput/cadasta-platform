from jsonattrs.models import Schema

from organization.views.mixins import ProjectMixin
from party.models import Party, TenureRelationship, TENURE_RELATIONSHIP_TYPES
from spatial.models import SpatialUnit
from resources.models import Resource
from spatial.choices import TYPE_CHOICES


class SearchResultsMixin(ProjectMixin):
    def format_search_results(self, results):
        search_results = []
        model_key = {
            'location': SpatialUnit,
            'party': Party,
            'tenure_rel': TenureRelationship,
            'resource': Resource
        }

        for result in results['hits']['hits']:
            result_model = model_key[result['_type']]
            _result = self.format_result(model=result_model, result=result)

            search_results.append(_result)

        return search_results

    def format_result(self, model, result):
        entity = self._get_entity(model, result)

        _result = {}
        _result['main_label'] = self._get_main_label(model, result)
        _result['entity_type'] = entity.ui_class_name
        _result['url'] = entity.ui_detail_url
        _result['main_label'] = self._get_main_label(model, result)
        _result['attributes'] = self._get_attributes(entity, result)

        if model == Resource:
            _result['image'] = entity._original_url

        return _result

    def _get_entity(self, model, result):
        return model.objects.get(id=result['_id'])

    def _get_attributes(self, entity, result):
        if type(entity) == Resource:
            attributes = [
                ("Original File", result['_source']['original_file']),
                ("Description", result['_source']['description'])]
        else:
            schema = Schema.objects.from_instance(entity)
            attrs = [a for s in schema for a in s.attributes.all()]
            attributes = [(a.long_name, a.render(
                          entity.attributes.get(a.name, '—')))
                          for a in attrs if not a.omit]

        return attributes

    def _get_main_label(self, model, result):
        if model == TenureRelationship:
            for key, item in TENURE_RELATIONSHIP_TYPES:
                if key == result['_source']['tenure_type']:
                    main_label = item

        elif model == SpatialUnit:
            for key, item in TYPE_CHOICES:
                if key == result['_source']['type']:
                    main_label = item

        else:
            main_label = result['_source']['name']

        return main_label

    def get_results_total(self, results):
        return results['hits']['total']
