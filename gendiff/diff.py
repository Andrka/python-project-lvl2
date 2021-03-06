# -*- coding:utf-8 -*-

"""Find diff."""

NESTED = 'nested'
ADDED = 'added'
DELETED = 'deleted'
CHANGED = 'changed'
SAME = 'same'

from gendiff import files, format  # noqa: E402


def printable(
    old_file: str,
    new_file: str,
    output_format: str = format.DEFAULT,
) -> str:
    """Generate and return diff between two files.

    Raises:
        ValueError: unsupported output format.

    """
    first_file = files.load(old_file)
    second_file = files.load(new_file)
    diff = compare(first_file, second_file)
    if output_format == format.DEFAULT:
        return format.default(diff)
    if output_format == format.PLAIN:
        return format.plain(diff)
    if output_format == format.JSON:
        return format.json(diff)
    raise ValueError('Unsupported output format!')


def compare(first_file: dict, second_file: dict) -> dict:  # noqa: WPS210
    """Create dict with diff between two files."""
    diff_result = {}
    common_keys = first_file.keys() & second_file.keys()
    for key in common_keys:
        old_value = first_file[key]
        new_value = second_file[key]
        if old_value == new_value:
            diff_result[key] = (SAME, old_value)  # noqa: WPS204
        elif (  # noqa: WPS337
            isinstance(old_value, dict)
                and isinstance(new_value, dict)  # noqa: W503
            ):
            diff_result[key] = (NESTED, compare(
                old_value,
                new_value,
            ))
        else:
            diff_result[key] = (CHANGED, (old_value, new_value))
    deleted_keys = first_file.keys() - second_file.keys()
    for key in deleted_keys:  # noqa: WPS440
        diff_result[key] = (DELETED, first_file[key])  # noqa: WPS441
    added_keys = second_file.keys() - first_file.keys()
    for key in added_keys:  # noqa: WPS440
        diff_result[key] = (ADDED, second_file[key])  # noqa: WPS441
    return diff_result
