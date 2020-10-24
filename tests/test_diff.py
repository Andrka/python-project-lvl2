# -*- coding:utf-8 -*-

"""Test diff module."""

import pytest

from gendiff import format
from gendiff.diff import compare, printable

OLD_JSON_PATH = 'tests/fixtures/old.json'
NEW_JSON_PATH = 'tests/fixtures/new.json'
OLD_YAML_PATH = 'tests/fixtures/old.yml'
NEW_YAML_PATH = 'tests/fixtures/new.yml'


@pytest.mark.parametrize(
    'expected_result, old_file, new_file, output_format',
    [
        ('diff_default_txt', OLD_JSON_PATH, NEW_JSON_PATH, format.DEFAULT),
        ('diff_default_txt', OLD_YAML_PATH, NEW_YAML_PATH, format.DEFAULT),
        ('diff_plain_txt', OLD_JSON_PATH, NEW_JSON_PATH, format.PLAIN),
        ('diff_plain_txt', OLD_YAML_PATH, NEW_YAML_PATH, format.PLAIN),
        ('diff_json_txt', OLD_JSON_PATH, NEW_JSON_PATH, format.JSON),
        ('diff_json_txt', OLD_YAML_PATH, NEW_YAML_PATH, format.JSON),
    ],
)
def test_printable_with_format(
    request,
    expected_result,
    old_file,
    new_file,
    output_format,
):
    """Test printable function with output format."""
    expected_diff = request.getfixturevalue(expected_result)
    test_diff = printable(
        old_file,
        new_file,
        output_format,
    )
    assert test_diff == expected_diff


@pytest.mark.parametrize(
    'expected_result, old_file, new_file',
    [
        ('diff_default_txt', OLD_JSON_PATH, NEW_JSON_PATH),
        ('diff_default_txt', OLD_YAML_PATH, NEW_YAML_PATH),
    ],
)
def test_printable_without_format(
    request,
    expected_result,
    old_file,
    new_file,
):
    """Test printable function without output format."""
    expected_diff = request.getfixturevalue(expected_result)
    test_diff = printable(
        old_file,
        new_file,
    )
    assert test_diff == expected_diff


@pytest.mark.parametrize(
    'old_file, new_file',
    [
        ('old_json', 'new_json'),
        ('old_yml', 'new_yml'),
    ],
)
def test_compare(diff, request, old_file, new_file):
    """Test compare function."""
    assert compare(
        request.getfixturevalue(old_file),
        request.getfixturevalue(new_file),
    ) == diff
