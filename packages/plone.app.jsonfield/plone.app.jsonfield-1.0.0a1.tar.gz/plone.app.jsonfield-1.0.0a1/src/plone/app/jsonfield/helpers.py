# _*_ coding: utf-8 _*_
from plone.app.jsonfield.compat import _
from plone.app.jsonfield.compat import json
from zope.interface import Invalid

import six
import sys


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


def parse_json_str(str_val, encoding='utf-8'):
    """ """
    try:
        json_dict = json.loads(str_val, encoding=encoding)
    except ValueError as exc:
        six.reraise(Invalid, Invalid(_('Invalid JSON String is provided!\n{0!s}').format(exc)), sys.exc_info()[2])

    return json_dict
