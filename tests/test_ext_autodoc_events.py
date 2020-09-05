"""
    test_ext_autodoc_events
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly for autodoc events

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from sphinx.ext.autodoc import between, cut_lines
from test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_process_docstring(app):
    def on_process_docstring(app, what, name, obj, options, lines):
        lines.clear()
        lines.append('my docstring')

    app.connect('autodoc-process-docstring', on_process_docstring)

    actual = do_autodoc(app, 'function', 'target.process_docstring.func')
    assert list(actual) == [
        '',
        '.. py:function:: func()',
        '   :module: target.process_docstring',
        '',
        '   my docstring'
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_cut_lines(app):
    app.connect('autodoc-process-docstring',
                cut_lines(2, 2, ['function']))

    actual = do_autodoc(app, 'function', 'target.process_docstring.func')
    assert list(actual) == [
        '',
        '.. py:function:: func()',
        '   :module: target.process_docstring',
        '',
        '   second line',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_between(app):
    app.connect('autodoc-process-docstring',
                between('---', ['function']))

    actual = do_autodoc(app, 'function', 'target.process_docstring.func')
    assert list(actual) == [
        '',
        '.. py:function:: func()',
        '   :module: target.process_docstring',
        '',
        '   second line',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_between_exclude(app):
    app.connect('autodoc-process-docstring',
                between('---', ['function'], exclude=True))

    actual = do_autodoc(app, 'function', 'target.process_docstring.func')
    assert list(actual) == [
        '',
        '.. py:function:: func()',
        '   :module: target.process_docstring',
        '',
        '   first line',
        '   third line',
        '',
    ]
