# -*- coding:utf-8 -*-

"""Test json_format module."""

from gendiff.file_loader import open_file
from gendiff.formatters.json_format import prepare_to_json_format

diff = open_file('tests/fixtures/diff.json')
expected_result = open_file('tests/fixtures/diff_json.txt')


def test_prepare_to_json_format():
    """Test prepare_to_json_format function."""
    sample_diff = set(expected_result.split('\n'))
    test_diff = set(prepare_to_json_format(diff).split('\n'))
    assert sample_diff == test_diff