# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.jsonfield import value
from plone.app.jsonfield.helpers import parse_json_str
from zope.interface import Invalid
from zope.schema import NO_VALUE
from zope.schema.interfaces import WrongType

import json
import os
import six
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class ValueIntegrationTest(unittest.TestCase):
    """ """
    def test_json_value(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            iter_value = json.load(f)

        json_value = value.JSONObjectValue(iter_value)
        self.assertIsInstance(json_value.stringify(), six.string_types)

        json_arry_str = """
        [
            {"hello": "hp"}
        ]
        """
        json_value = value.JSONObjectValue(iter_value)
        self.assertIsInstance(json_value.stringify(), six.string_types)

        # Test Patch
        patch_data = {'hello': 123}
        try:
            json_value.patch(patch_data)
            raise AssertionError('Code should not come here! because wrong type data is provided for patch!')
        except WrongType:
            pass
        patch_data = [
            {'path': '/text/fake path', 'value': 'patched!', 'Invalid Option': 'replace'}
        ]
        # Test getting original error from json patcher
        try:
            json_value.patch(patch_data)
            raise AssertionError(
                'Code should not come here! because wrong patch data is provided for patch and invalid format as well!'
            )
        except Invalid as exc:
            self.assertIn("does not contain 'op' member", str(exc))

        patch_data = [
            {'path': '/text/status', 'value': 'patched!', 'op': 'replace'}
        ]
        json_value.patch(patch_data)

        self.assertEqual('patched!', json_value['text']['status'])

        # Make sure string is transformable to fhir resource
        json_str = json_value.stringify()
        json_dict = parse_json_str(json_str)

        empty_resource = value.JSONObjectValue(NO_VALUE)
        # __bool__ should be False
        self.assertFalse(empty_resource)

        # Test Patch with empty value
        try:
            empty_resource.patch(patch_data)
            raise AssertionError('Code should not come here! because empty json cannot be patched!')
        except Invalid:
            pass

        self.assertIn('{}', repr(empty_resource))
        self.assertEqual('{}', str(empty_resource))

        # Validation Test:: more explict with schema???
        try:
            value.JSONObjectValue('Ketty')
            raise AssertionError('Code should not come here, because should raise validation error!')
        except WrongType:
            pass
