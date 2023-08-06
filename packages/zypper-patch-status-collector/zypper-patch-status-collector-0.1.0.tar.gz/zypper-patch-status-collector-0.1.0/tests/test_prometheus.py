import re

from zypper_patch_status_collector._model import CATEGORIES, SEVERITIES, Patch
from zypper_patch_status_collector._prometheus import render

# Expect all category-severity combinations and the zypper query failed metric
EXPECTED_METRICS_COUNT = len(CATEGORIES) * len(SEVERITIES) + 1


def _parse_metrics(metrics):
    parsed = {}

    for line in metrics.splitlines():
        metric_match = re.match(r'^(?P<metric>\S+)\s+(?P<value>\S+)$', line)
        if metric_match:
            parsed[metric_match.group('metric')] = float(metric_match.group('value'))

    return parsed


def test_render_no_patches():
    patches = []

    metrics = render(patches)

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT
    assert parsed_metrics.pop('zypper_scrape_success') == 1
    for value in parsed_metrics.values():
        assert value == 0


def test_render_multiple_patches():
    patches = [
        Patch('security', 'important'),
        Patch('optional', 'moderate'),
        Patch('security', 'important'),
    ]

    metrics = render(patches)

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT
    assert parsed_metrics['zypper_applicable_patches{category="security",severity="important"}'] == 2
    assert parsed_metrics['zypper_applicable_patches{category="optional",severity="moderate"}'] == 1
    assert parsed_metrics['zypper_applicable_patches{category="feature",severity="low"}'] == 0
    assert parsed_metrics['zypper_scrape_success'] == 1


def test_render_failure():
    patches = None

    metrics = render(patches)

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == 1
    assert parsed_metrics['zypper_scrape_success'] == 0
