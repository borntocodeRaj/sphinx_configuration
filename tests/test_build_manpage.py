"""
    test_build_manpage
    ~~~~~~~~~~~~~~~~~~

    Test the build process with manpage builder with the test root.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from sphinx.builders.manpage import default_man_pages
from sphinx.config import Config


@pytest.mark.sphinx('man')
def test_all(app, status, warning):
    app.builder.build_all()
    assert (app.outdir / 'sphinxtests.1').exists()

    content = (app.outdir / 'sphinxtests.1').read_text()
    assert r'\fBprint \fP\fIi\fP\fB\en\fP' in content
    assert r'\fBmanpage\en\fP' in content

    # term of definition list including nodes.strong
    assert '\n.B term1\n' in content
    assert '\nterm2 (\\fBstronged partially\\fP)\n' in content

    assert 'Footnotes' not in content


@pytest.mark.sphinx('man', testroot='directive-code')
def test_captioned_code_block(app, status, warning):
    app.builder.build_all()
    content = (app.outdir / 'python.1').read_text()

    assert ('.sp\n'
            'caption \\fItest\\fP rb\n'
            '.INDENT 0.0\n'
            '.INDENT 3.5\n'
            '.sp\n'
            '.nf\n'
            '.ft C\n'
            'def ruby?\n'
            '    false\n'
            'end\n'
            '.ft P\n'
            '.fi\n'
            '.UNINDENT\n'
            '.UNINDENT\n' in content)


def test_default_man_pages():
    config = Config({'project': 'STASI™ Documentation',
                     'author': "Wolfgang Schäuble & G'Beckstein",
                     'release': '1.0'})
    config.init_values()
    expected = [('index', 'stasi', 'STASI™ Documentation 1.0',
                 ["Wolfgang Schäuble & G'Beckstein"], 1)]
    assert default_man_pages(config) == expected


@pytest.mark.sphinx('man', testroot='markup-rubric')
def test_rubric(app, status, warning):
    app.build()
    content = (app.outdir / 'python.1').read_text()
    assert 'This is a rubric\n' in content
