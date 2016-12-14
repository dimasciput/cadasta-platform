import json

from unittest.mock import patch
from django.conf import settings
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied
from tutelary.models import Policy, assign_user_policies
from skivvy import APITestCase

from accounts.tests.factories import UserFactory
from core.tests.utils.cases import UserTestCase
from organization.tests.factories import ProjectFactory
from spatial.tests.factories import SpatialUnitFactory
from ..views import api


api_url = (
    settings.ES_SCHEME + '://' + settings.ES_HOST + ':' + settings.ES_PORT)


def assign_policies(user):
    clauses = {
        'clause': [
            {
                'effect': 'allow',
                'object': ['project/*/*'],
                'action': ['project.view_private']
            },
        ],
    }
    policy = Policy.objects.create(
        name='test-policy',
        body=json.dumps(clauses))
    assign_user_policies(user, policy)


class SearchAPITest(APITestCase, UserTestCase, TestCase):
    view_class = api.Search

    def setup_models(self):
        self.user = UserFactory.create()
        assign_policies(self.user)
        self.project = ProjectFactory.create(slug='test-project')

    def setup_url_kwargs(self):
        return {
            'organization': self.project.organization.slug,
            'project': self.project.slug,
        }

    @patch('requests.post')
    def test_query_es(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'hits': {
                'total': 0,
                'hits': [],
            },
        }

        query = 'none'
        view = self.view_class()
        r = view.query_es(query, self.project.slug)

        body = {'query': {'simple_query_string': {
            'default_operator': 'and',
            'query': query,
        }}}
        mock_post.assert_called_once_with(
            '{}/{}/_search'.format(api_url, self.project.slug),
            data=json.dumps(body, sort_keys=True),
        )
        assert r.json() == mock_post.return_value.json.return_value

    @patch('requests.post')
    def test_get_with_valid_user_and_no_results(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'hits': {
                'total': 0,
                'hits': [],
            },
        }

        query = 'none'
        response = self.request(user=self.user,
                                get_data={'q': query})
        assert response.status_code == 200
        assert response.content['results'] == []

        body = {'query': {'simple_query_string': {
            'default_operator': 'and',
            'query': query,
        }}}
        mock_post.assert_called_once_with(
            '{}/{}/_search'.format(api_url, self.project.slug),
            data=json.dumps(body, sort_keys=True),
        )

    @patch('requests.post')
    def test_get_with_valid_user_and_with_results(self, mock_post):
        su = SpatialUnitFactory.create(project=self.project)

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'hits': {
                'total': 0,
                'hits': [
                    {
                        '_type': 'location',
                        '_id': su.id,
                    },
                ],
            },
        }

        query = 'none'
        response = self.request(user=self.user,
                                get_data={'q': query})
        assert response.status_code == 200
        assert response.content['results'] == [[
            su.ui_class_name,
            '<a href="{}">{}</a>'.format(su.ui_detail_url, su.name),
        ]]

        body = {'query': {'simple_query_string': {
            'default_operator': 'and',
            'query': query,
        }}}
        mock_post.assert_called_once_with(
            '{}/{}/_search'.format(api_url, self.project.slug),
            data=json.dumps(body, sort_keys=True),
        )

    @patch('requests.post')
    def test_get_with_valid_user_and_missing_query(self, mock_post):
        response = self.request(user=self.user)
        assert response.status_code == 200
        assert response.content['results'] == []
        mock_post.assert_not_called()

    def test_get_with_nonexistent_org(self):
        response = self.request(user=self.user,
                                url_kwargs={'organization': 'evil-corp'})
        assert response.status_code == 404
        assert response.content['detail'] == "Project not found."

    def test_get_with_nonexistent_project(self):
        response = self.request(user=self.user,
                                url_kwargs={'project': 'world-domination'})
        assert response.status_code == 404
        assert response.content['detail'] == "Project not found."

    def test_get_with_unauthorized_user(self):
        response = self.request()
        assert response.status_code == 403
        assert response.content['detail'] == PermissionDenied.default_detail
