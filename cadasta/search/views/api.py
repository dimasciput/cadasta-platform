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


class Search(APIPermissionRequiredMixin,
             ProjectMixin,
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

            # Add more detail to search results
            for result in r.json()['hits']['hits']:
                rec_type = result['_type']
                id = result['_id']
                model = {
                    'location': SpatialUnit,
                    'party': Party,
                    'tenure_rel': TenureRelationship,
                    'resource': Resource,
                }[rec_type]
                record = model.objects.get(id=id)
                # TODO: Perform Tutelary permissions checking
                result['ui_class_name'] = record.ui_class_name
                result['ui_detail_url'] = record.ui_detail_url
                result['ui_name'] = record.name
                results.append(result)

        return Response({'results': results})
