def mock_zypper_call(mocker, result_filename):
    mock = mocker.patch(
        'subprocess.check_output'
    )
    mock.return_value = open(result_filename).read()
    return mock


def assert_zypper_mock_use(mock):
    assert mock.call_args[0][0][0] == 'zypper'
    assert mock.call_args[0][0][-1] == 'list-patches'
    assert '--xmlout' in mock.call_args[0][0]
