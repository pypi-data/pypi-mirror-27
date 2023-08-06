import collections
import itertools

from ._model import CATEGORIES, SEVERITIES, Patch


GAUGE_META_TEMPLATE = '''\
# HELP {name} {help_text}
# TYPE {name} gauge
'''


GAUGE_VALUE_TEMPLATE = '''\
{name} {value}
'''


def _render_gauge_meta(name, help_text):
    return GAUGE_META_TEMPLATE.format(
        name=name,
        help_text=help_text
    )


def _render_gauge_value(name, value):
    return GAUGE_VALUE_TEMPLATE.format(
        name=name,
        value=value,
    )


def _render_patch_meta():
    return _render_gauge_meta(
        name='zypper_applicable_patches',
        help_text='The current count of applicable patches',
    )


def _render_patch_count(patch, count):
    return _render_gauge_value(
        name='zypper_applicable_patches{{category="{category}",severity="{severity}"}}'.format(
            category=patch.category,
            severity=patch.severity,
        ),
        value=count,
    )


def _render_scrape_success(value):
    return _render_gauge_meta(
        name='zypper_scrape_success',
        help_text='Whether the last scrape for zypper data was successful.',
    ) + _render_gauge_value(
        name='zypper_scrape_success',
        value=value,
    )


def render(patches):
    patch_histogram = collections.Counter(patches)

    if patches is None:
        return _render_scrape_success(0)

    metrics = [
        _render_patch_meta()
    ] + [
        _render_patch_count(patch, patch_histogram.get(patch, 0))
        for patch in (
            Patch(category, severity) for category, severity in itertools.product(CATEGORIES, SEVERITIES)
        )
    ] + [
        _render_scrape_success(1)
    ]
    return ''.join(metrics)
