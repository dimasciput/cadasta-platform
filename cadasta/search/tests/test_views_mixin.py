from django.test import TestCase
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from questionnaires.managers import create_attrs_schema
from questionnaires.tests.attr_schemas import (individual_party_xform_group,
                                               default_party_xform_group,
                                               tenure_relationship_xform_group)
from questionnaires.tests.factories import QuestionnaireFactory
from core.tests.utils.cases import UserTestCase
from spatial.tests.factories import SpatialUnitFactory
from spatial.models import SpatialUnit
from party.tests.factories import PartyFactory, TenureRelationshipFactory
from party.models import Party, TenureRelationship
from resources.tests.factories import ResourceFactory
from resources.models import Resource
from organization.tests.factories import ProjectFactory
from ..views.mixins import SearchResultsMixin as mixin
from .fake_results import get_test_results


class SearchResultsMixinTest(UserTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory.create()
        QuestionnaireFactory.create(project=self.project)
        content_type = ContentType.objects.get(
            app_label='party', model='party')
        create_attrs_schema(
            project=self.project, dict=individual_party_xform_group,
            content_type=content_type, errors=[])
        create_attrs_schema(
            project=self.project, dict=default_party_xform_group,
            content_type=content_type, errors=[])

        content_type = ContentType.objects.get(
            app_label='party', model='tenurerelationship')
        create_attrs_schema(
            project=self.project, dict=tenure_relationship_xform_group,
            content_type=content_type, errors=[])

        self.su = SpatialUnitFactory.create(project=self.project)
        self.party = PartyFactory.create(
            project=self.project,
            type='IN',
            attributes={
                'gender': 'm',
                'homeowner': 'yes',
                'dob': '1951-05-05'
            })
        self.tenure_rel = TenureRelationshipFactory.create(
            spatial_unit=self.su, party=self.party, project=self.project,
            attributes={'notes': 'PBS is the best.'})
        self.resource = ResourceFactory.create(project=self.project)

        self.results = get_test_results(
            self.su, self.party, self.tenure_rel, self.resource)
        self.su_result = self.results['hits']['hits'][0]
        self.party_result = self.results['hits']['hits'][1]
        self.tenure_rel_result = self.results['hits']['hits'][2]
        self.resource_result = self.results['hits']['hits'][3]

    def test_format_search_results(self):
        search_results = mixin().format_search_results(self.results)
        assert len(search_results) == 4

    def test_format_result_spatial_unit(self):
        final_result = mixin().format_result(type(self.su), self.su_result)
        assert final_result['entity_type'] == _('Location')
        assert final_result['url'] == (
            '/organizations/{org}/projects/{proj}/records/locations/{record}/'
            ).format(org=self.project.organization.slug,
                     proj=self.project.slug, record=self.su.id)
        assert final_result['attributes'] == []
        assert final_result['main_label'] == _('Community boundary')

    def test_format_result_party(self):
        final_result = mixin().format_result(
            type(self.party), self.party_result)

        assert final_result['entity_type'] == _('Party')
        assert final_result['url'] == (
            '/organizations/{org}/projects/{proj}/records/parties/{record}/'
            ).format(org=self.project.organization.slug,
                     proj=self.project.slug, record=self.party.id)
        assert ('Notes', '—') in final_result['attributes']
        assert ('Gender', 'Male') in final_result['attributes']
        assert ('Homeowner', 'Yes') in final_result['attributes']
        assert ('Date of Birth', '1951-05-05') in final_result['attributes']
        assert final_result['main_label'] == _('Big Bird')

    def test_format_result_tenure_relationship(self):
        final_result = mixin().format_result(
            type(self.tenure_rel), self.tenure_rel_result)

        assert final_result['entity_type'] == _('Relationship')
        assert final_result['url'] == (
            '/organizations/{org}/projects/{proj}/relationships/{record}/'
            ).format(org=self.project.organization.slug,
                     proj=self.project.slug, record=self.tenure_rel.id)
        assert ('Notes', 'PBS is the best.') in final_result['attributes']
        assert final_result['main_label'] == _('Customary Rights')

    def test_format_result_resource(self):
        final_result = mixin().format_result(
            type(self.resource), self.resource_result)

        assert final_result['entity_type'] == _('Resource')
        assert final_result['url'] == (
            '/organizations/{org}/projects/{proj}/resources/{record}/'
            ).format(org=self.project.organization.slug,
                     proj=self.project.slug, record=self.resource.id)
        assert ('Original File', 'baby_goat.jpeg'
                ) in final_result['attributes']
        assert ('Description', "Let's pretend there's a description."
                ) in final_result['attributes']
        assert final_result['main_label'] == _('Goat')
        assert final_result['image'] == self.resource._original_url

    def test_get_entity_spatial_unit(self):
        entity = mixin()._get_entity(SpatialUnit, self.su_result)
        assert entity == self.su

    def test_get_entity_party(self):
        entity = mixin()._get_entity(Party, self.party_result)
        assert entity == self.party

    def test_get_entity_tenure_relationship(self):
        entity = mixin()._get_entity(
            TenureRelationship, self.tenure_rel_result)
        assert entity == self.tenure_rel

    def test_get_entity_resource(self):
        entity = mixin()._get_entity(Resource, self.resource_result)
        assert entity == self.resource

    def test_get_attributes_spatial_unit(self):
        attributes = mixin()._get_attributes(self.su, self.su_result)
        assert len(attributes) == 0

    def test_get_attributes_party(self):
        attributes = mixin()._get_attributes(self.party, self.party_result)
        assert ('Notes', '—') in attributes
        assert ('Gender', 'Male') in attributes
        assert ('Homeowner', 'Yes') in attributes
        assert ('Date of Birth', '1951-05-05') in attributes

    def test_get_attributes_tenure_relationship(self):
        attributes = mixin()._get_attributes(
            self.tenure_rel, self.tenure_rel_result)
        assert ('Notes', 'PBS is the best.') in attributes

    def test_get_attributes_resource(self):
        attributes = mixin()._get_attributes(
            self.resource, self.resource_result)
        assert ('Original File', 'baby_goat.jpeg'
                ) in attributes
        assert ('Description', "Let's pretend there's a description."
                ) in attributes

    def test_get_main_label_spatial_unit(self):
        main_label = mixin()._get_main_label(SpatialUnit, self.su_result)
        assert main_label == _("Community boundary")

    def test_get_main_label_party(self):
        main_label = mixin()._get_main_label(Party, self.party_result)
        assert main_label == _("Big Bird")

    def test_get_main_label_tenure_relationship(self):
        main_label = mixin()._get_main_label(
            TenureRelationship, self.tenure_rel_result)
        assert main_label == _("Customary Rights")

    def test_get_main_label_resource(self):
        main_label = mixin()._get_main_label(Resource, self.resource_result)
        assert main_label == _("Goat")

    def test_get_results_total(self):
        results_total = mixin().get_results_total(self.results)
        assert results_total == 4
