# _*_ coding: utf-8 _*_
from . import FHIR_FIXTURE_PATH
from plone.app.jsonfield import field
from plone.app.jsonfield.interfaces import IJSONValue
from plone.app.jsonfield.value import JSONObjectValue
from zope.interface import Invalid
from zope.schema._bootstrapinterfaces import ConstraintNotSatisfied
from zope.schema.interfaces import WrongContainedType
from zope.schema.interfaces import WrongType

import json
import os
import six
import unittest


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


class FieldIntegrationTest(unittest.TestCase):
    """ """

    def test_init_validate(self):  # noqa: C901
        """ """
        # Test with minimal params
        try:
            field.JSON(
                title=six.text_type('Organization resource'),
            )
        except Invalid as exc:
            raise AssertionError('Code should not come here, as everything should goes fine.\n{0!s}'.format(exc))

        # Explict error test?

    def test_from_iterable(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_dict = json.load(f)

        fhir_field = field.JSON(
            title=six.text_type('Organization resource')
        )

        try:
            fhir_resource_value = fhir_field.from_iterable(json_dict)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid JSONValue.\n{0!s}'.format(exc)
                )

        self.assertEqual(fhir_resource_value['resourceType'], json_dict['resourceType'])

    def test_fromUnicode(self):
        """ """
        with open(os.path.join(FHIR_FIXTURE_PATH, 'Organization.json'), 'r') as f:
            json_str = f.read()

        fhir_field = field.JSON(
            title=six.text_type('Organization resource')
        )

        try:
            fhir_field.fromUnicode(json_str)
        except Invalid as exc:
            raise AssertionError(
                'Code should not come here! as should return valid JSONValue.\n{0!s}'.format(exc)
                )

        # Test with invalid json string
        try:
            invalid_data = '{hekk: invalg, 2:3}'
            fhir_field.fromUnicode(invalid_data)
            raise AssertionError('Code should not come here! invalid json string is provided')
        except Invalid as exc:
            self.assertIn('Invalid JSON String', str(exc))
