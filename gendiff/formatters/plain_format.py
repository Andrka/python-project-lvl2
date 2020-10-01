# -*- coding:utf-8 -*-

"""Generate plain text diff between two files."""

from gendiff.constants import ADDED, CHANGED, DELETED, NESTED
from gendiff.formatters.converter import convert_to_json_veiw


def prepare_to_plain_format(  # noqa: WPS231, WPS210
    diff: dict,
    path_to_root: str = '',
    ) -> str:
    """Convert given diff to plain text format."""
    diff_in_list = []
    for key, key_parameter in diff.items():
        if isinstance(key_parameter, list):
            if key_parameter[0] == NESTED:
                diff_in_list.append(
                    prepare_to_plain_format(
                        key_parameter[1],  # noqa: WPS204
                        '{0}{1}{2}'.format(
                            path_to_root,
                            '.' if path_to_root else '',
                            key,
                        ),
                    ),
                )
            if key_parameter[0] == ADDED:
                current_value = key_parameter[1]
                if isinstance(current_value, dict):
                    current_value = '[complex value]'
                elif not isinstance(current_value, bool):
                    current_value = "'{0}'".format(current_value)
                new_line = (
                    "Property '{0}' was added with value: {1}"
                ).format(
                    '{0}{1}{2}'.format(
                        path_to_root,
                        '.' if path_to_root else '',
                        key,
                    ),
                    convert_to_json_veiw(current_value),
                )
                diff_in_list.append(new_line)
            if key_parameter[0] == DELETED:
                new_line = "Property '{0}' was removed".format(
                    '{0}{1}{2}'.format(
                        path_to_root,
                        '.' if path_to_root else '',
                        key,
                    ),
                )
                diff_in_list.append(new_line)
            if key_parameter[0] == CHANGED:
                current_value = key_parameter[2]
                if isinstance(current_value, dict):
                    current_value = '[complex value]'
                elif not isinstance(current_value, bool):
                    current_value = "'{0}'".format(current_value)
                old_value = key_parameter[1]
                if isinstance(old_value, dict):
                    old_value = '[complex value]'
                elif not isinstance(old_value, bool):
                    old_value = "'{0}'".format(old_value)
                new_line = (
                    "Property '{0}' was updated. From {1} to {2}"
                ).format(
                    '{0}{1}{2}'.format(
                        path_to_root,
                        '.' if path_to_root else '',
                        key,
                    ),
                    convert_to_json_veiw(old_value),
                    convert_to_json_veiw(current_value),
                )
                diff_in_list.append(new_line)
    return '\n'.join(diff_in_list)