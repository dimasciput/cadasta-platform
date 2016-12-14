from jsonattrs.models import Schema

from organization.views.mixins import ProjectMixin
from party.models import Party, TenureRelationship, TENURE_RELATIONSHIP_TYPES
from spatial.models import SpatialUnit
from resources.models import Resource
from spatial.choices import TYPE_CHOICES


class SearchResultsMixin(ProjectMixin):
    def _format_search_results(self):
        location_schema = False
        party_schema = False
        tenure_schema = False

        initial_results = {
          "took": 63,
          "timed_out": 'false',
          "_shards": {
            "total": 5,
            "successful": 5,
            "failed": 0
          },
          "hits": {
            "total": 1000,
            "max_score": 'null',
            "hits": [{
              "_index": "project-slug",
              "_type": "location",
              "_id": "2tmu6m59z56k3f9b2i4j5htx",
              "sort": [0],
              "_score": 'null',
              "_source": {
                "type": "CB",
                "name": "Long Island",
                "notes": "Nothing to see here.",
                "acquired_when": "2016-12-16",
                "quality": "text",
                "acquired_how": "LH"}
            }, {
              "_index": "project-slug",
              "_type": "party",
              "_id": "rjy3gfuar8cx2rqa9gtu8f52",
              "sort": [1],
              "_score": 'null',
              "_source": {
                "name": "Big Bird",
                "type": "IN",
                "notes": ("He\'s just a big bird. "
                          "Not the guy from seasame street..")}
            }, {
              "_index": "project-slug",
              "_type": "tenure_rel",
              "_id": "nhnrzxgrwvxrgb4qgxq9ke7j",
              "sort": [1],
              "_score": 'null',
              "_source": {
                "party": "rjy3gfuar8cx2rqa9gtu8f52",
                "spatial_unit": "2tmu6m59z56k3f9b2i4j5htx",
                "tenure_type": "CU",
                "notes": "But he does have customary rights."}
            }, {
              "_index": "project-slug",
              "_type": "resource",
              "_id": "9bhr7hvtwnppynuvr5yg3wjd",
              "sort": [1],
              "_score": 'null',
              "_source": {
                "name": "Goat",
                "description": "Let's pretend there's a description.",
                "original_file": "baby_goat.jpeg"}
            },
            ]
          }
        }
        search_results = []
        for result in initial_results['hits']['hits']:
            if result['_type'] == 'location':
                _result = self.format_result(
                    entity_type='Location',
                    entity_model=SpatialUnit,
                    entity_id=result['_id'],
                    schema=location_schema,
                    choices=TYPE_CHOICES,
                    entity_label=result['_source']['type'])
                _result['url'] = 'locations:detail'
                _result['url_variable'] = result['_id']
                search_results.append(_result)

            elif result['_type'] == 'party':
                _result = self.format_result(
                    entity_type='Party',
                    entity_model=Party,
                    entity_id=result['_id'],
                    schema=party_schema,
                    choices=None,
                    entity_label=result['_source']['name'])
                _result['url'] = 'parties:detail'
                _result['url_variable'] = result['_id']
                search_results.append(_result)

            elif result['_type'] == 'resource':
                _result = {}
                _result['entity_type'] = 'Resource'
                _result['attributes'] = [
                    ("Description", result['_source']['description'])]
                _result['main_label'] = result['_source']['name']
                _result['url'] = 'resources:project_detail'
                _result['url_variable'] = result['_id']
                search_results.append(_result)

            elif result['_type'] == 'tenure_rel':
                _result = self.format_result(
                    entity_type='Tenure Relationship',
                    entity_model=TenureRelationship,
                    entity_id=result['_id'],
                    schema=tenure_schema,
                    choices=TENURE_RELATIONSHIP_TYPES,
                    entity_label=result['_source']['tenure_type'])
                _result['url'] = 'parties:relationship_detail'
                _result['url_variable'] = result['_id']
                search_results.append(_result)

        return search_results

    def format_result(self, entity_type, entity_model, entity_id, schema,
                      choices, entity_label):
        entity = entity_model.objects.get(id=entity_id)
        _result = {}

        if not schema:
            schema = Schema.objects.from_instance(entity)

        attrs = [a for s in schema for a in s.attributes.all()]
        _result['attributes'] = [
            (a.long_name, a.render(
             entity.attributes.get(a.name, '—')))
            for a in attrs if not a.omit]

        _result['entity_type'] = entity_type
        if choices:
            for key, item in choices:
                if key == entity_label:
                    _result['main_label'] = item
        else:
            _result['main_label'] = entity_label

        return _result
