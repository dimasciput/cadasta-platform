import requests
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from tutelary.mixins import APIPermissionRequiredMixin

from organization.views.mixins import ProjectMixin
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
        query = request.query_params.get('q')

        initial_results = self.format_search_results()
        results = []

        # if query:
        #     r = self.query_es(query, kwargs['project'])

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
            print(record)
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
