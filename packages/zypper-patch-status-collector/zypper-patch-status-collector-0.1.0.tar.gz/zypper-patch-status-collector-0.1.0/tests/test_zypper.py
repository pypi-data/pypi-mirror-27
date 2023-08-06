from zypper_patch_status_collector._zypper import Patch, get_applicable_patches

from .mock import assert_zypper_mock_use, mock_zypper_call


def test_no_patches(mocker):
    zypper_mock = mock_zypper_call(mocker, 'tests/fixtures/empty.xml')

    assert len(get_applicable_patches()) == 0

    assert_zypper_mock_use(zypper_mock)


def test_all_categories_and_severities(mocker):
    zypper_mock = mock_zypper_call(mocker, 'tests/fixtures/all.xml')

    patches = get_applicable_patches()
    assert len(patches) == 8
    assert Patch('security', 'important') in patches
    assert Patch('document', 'unspecified') in patches
    assert Patch('yast', 'important') not in patches

    assert_zypper_mock_use(zypper_mock)
