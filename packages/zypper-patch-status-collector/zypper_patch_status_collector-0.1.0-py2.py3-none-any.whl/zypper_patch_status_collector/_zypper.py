from __future__ import unicode_literals

import subprocess
import xml.etree.ElementTree as ET

from ._model import Patch


def _query_zypper():
    return subprocess.check_output([
        'zypper', '--xmlout', '--quiet', '--non-interactive', 'list-patches'
    ])


def _parse_zypper(patches_xml):
    root = ET.fromstring(patches_xml)
    patches = root.iter('update')
    return [
        Patch(patch.attrib.get('category'), patch.attrib.get('severity'))
        for patch in patches
    ]


def get_applicable_patches():
    patches_xml = _query_zypper()
    return _parse_zypper(patches_xml)
