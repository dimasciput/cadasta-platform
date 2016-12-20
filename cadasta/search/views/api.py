import requests
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from tutelary.mixins import APIPermissionRequiredMixin
from organization.models import Project
from spatial.models import SpatialUnit
from party.models import Party, TenureRelationship
from resources.models import Resource

from .mixins import SearchResultsMixin


class Search(APIPermissionRequiredMixin,
             SearchResultsMixin,
             APIView):

    permission_required = 'project.view_private'

    def get_perms_objects(self):
        return [self.get_project()]

    def query_es(self, query, project_slug):
        body = {'query': {'simple_query_string': {
            'default_operator': 'and',
            'query': query,
        }}}
        api = (
            settings.ES_SCHEME + '://' + settings.ES_HOST + ':' +
            settings.ES_PORT
        )
        r = requests.post(
            '{}/{}/_search'.format(api, project_slug),
            data=json.dumps(body, sort_keys=True),
        )
        assert r.status_code == 200
        return r

    def get(self, request, *args, **kwargs):
        print('ES get called.')
        query = request.query_params.get('q')
        results = []

        # if query:
        #     r = self.query_es(query, kwargs['project'])
        #     initial_results = self.format_search_results(r.json())

        # ~~~~~~~~~~~~~~~~~~~
        # JUST FOR TESTING
        # ~~~~~~~~~~~~~~~~~~~~
        su = SpatialUnit.objects.filter(project__slug=kwargs['project'])
        party = Party.objects.filter(project__slug=kwargs['project'])
        tenure_rel = TenureRelationship.objects.filter(project__slug=kwargs['project'])
        resource = Resource.objects.filter(project__slug=kwargs['project'])

        initial_results = get_test_results(su, party, tenure_rel, resource)
        initial_results = self.format_search_results(initial_results)

        for record in initial_results:
            html = (
             "<td>"
             "<table>"
             "<tr>"
             "<div>{entity_type}</div>"
             "<h4><a href='{url}'>{main_label}</a></h4>"
             "</tr>").format(
                entity_type=record['entity_type'],
                main_label=record['main_label'],
                url=record['url'])

            if record.get('image', None):
                html += (
                    '<tr>'
                    '<img src="{image}" class="thumb-60">'
                    '</tr>').format(
                        image=record['image'])

            for key, attr in record['attributes']:
                html += (
                  '<tr>'
                  '<td>{key}</td>'
                  '<td style="padding-left:50px;">{attr}</td>'
                  '</tr>').format(
                    key=key,
                    attr=attr)

            html += (
              '</table>'
              '</td>'
            )
            results.append([
                record['entity_type'],
                record['main_label'],
                html])

        return Response({'results': results})


# ~~~~~~~~~~~~~~~~~~~~~
# DELETE LATER
# ~~~~~~~~~~~~~~~~~~~~~

def get_test_results(spatial_units=[], parties=[],
                     tenure_rels=[], resources=[]):
    result = {
          "took": 63,
          "timed_out": 'false',
          "_shards": {
            "total": 4,
            "successful": 4,
            "failed": 0
          },
          "hits": {
            "total": 4,
            "max_score": 'null',
            "hits": []
          }
        }

    for su in spatial_units:
        result['hits']['hits'].append({
                "_index": su.project.id,
                "_type": "location",
                "_id": su.id,
                "sort": [0],
                "_score": 'null',
                "_source": {
                  "type": "CB",
                  "name": "Long Island",
                  "notes": "Nothing to see here.",
                  "acquired_when": "2016-12-16",
                  "quality": "text",
                  "acquired_how": "LH"}
              })
    for party in parties:
        result['hits']['hits'].append({
                "_index": party.project.slug,
                "_type": "party",
                "_id": party.id,
                "sort": [1],
                "_score": 'null',
                "_source": {
                  "name": "Big Bird",
                  "type": "IN",
                  "gender": "M",
                  "homeowner": "yes",
                  "dob": "1951-05-05"
                }
              })
    for tenure_rel in tenure_rels:
        result['hits']['hits'].append({
              "_index": tenure_rel.project.slug,
              "_type": "tenure_rel",
              "_id": tenure_rel.id,
              "sort": [1],
              "_score": 'null',
              "_source": {
                "party": "xqm9r3nymxv8pck52zgvz7t5",
                "spatial_unit": "zpeqs5uh39dhi8gr6ec3t3w5",
                "tenure_type": "CU",
                "notes": "PBS is the best."}
            })
    for resource in resources:
        result['hits']['hits'].append({
              "_index": resource.project.slug,
              "_type": "resource",
              "_id": resource.id,
              "sort": [1],
              "_score": 'null',
              "_source": {
                "name": resource.name,
                "description": resource.description,
                "original_file": resource.original_file}
            },)

    result['hits']['total'] = len(result['hits']['hits'])

    return result
