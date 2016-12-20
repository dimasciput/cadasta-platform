import requests
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from tutelary.mixins import APIPermissionRequiredMixin

from .mixins import SearchResultsMixin


# ~~~~~~~~~~~~~~~~
# Just for testing: DELETE later
# ~~~~~~~~~~~~~~~~
test_results = {
          "took": 63,
          "timed_out": 'false',
          "_shards": {
            "total": 5,
            "successful": 5,
            "failed": 0
          },
          "hits": {
            "total": 24,
            "max_score": 'null',
            "hits": [{
              "_index": "project-slug",
              "_type": "location",
              "_id": "zpeqs5uh39dhi8gr6ec3t3w5",
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
              "_id": "xqm9r3nymxv8pck52zgvz7t5",
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
              "_id": "3xcg8erv2yi22scm3kve8maa",
              "sort": [1],
              "_score": 'null',
              "_source": {
                "party": "xqm9r3nymxv8pck52zgvz7t5",
                "spatial_unit": "zpeqs5uh39dhi8gr6ec3t3w5",
                "tenure_type": "CU",
                "notes": "But he does have customary rights."}
            }, {
              "_index": "project-slug",
              "_type": "resource",
              "_id": "u25ayvgg57zqjrjkkshryyw5",
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
        query = request.query_params.get('q')
        results = []

        if query:
            r = self.query_es(query, kwargs['project'])
            print(r.json())
            initial_results = self.format_search_results(r.json())
            print(initial_results)

        #     # Parse and translate search results
        #     for result in r.json()['hits']['hits']:
        #         rec_type = result['_type']
        #         id = result['_id']
        #         model = {
        #             'location': SpatialUnit,
        #             'party': Party,
        #             'tenure_rel': TenureRelationship,
        #             'resource': Resource,
        #         }[rec_type]
        #         record = model.objects.get(id=id)
        #         # TODO: Perform Tutelary permissions checking
        #         results.append([
        #             record.ui_class_name,
        #             '<a href="{}">{}</a>'.format(
        #                 record.ui_detail_url,
        #                 record.name,
        #             ),
        #         ])

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
