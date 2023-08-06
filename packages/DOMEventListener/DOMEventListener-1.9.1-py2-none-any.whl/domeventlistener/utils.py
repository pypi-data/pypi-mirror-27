# -*- coding: utf-8 -*-
import difflib


def unidiff_output(expected, actual):
    """
    Returns a string containing the unified diff of two multiline strings.
    """

    expected = expected.splitlines(1)
    actual = actual.splitlines(1)

    diff = difflib.unified_diff(expected, actual)

    _diff = ''

    for d in list(diff):
        if type(d) == unicode:
            _diff += d
        else:
            _diff += d.decode('utf-8')

    return _diff
