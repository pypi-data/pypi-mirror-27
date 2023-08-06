# -*- coding: utf-8 -*-
"""Linter for Zope Page Templates."""

from __future__ import print_function
from zope.contentprovider.tales import TALESProviderExpression
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.tales.engine import Engine

import sys


def run():
    """Run ZPT Linter."""
    if len(sys.argv) < 2:
        print('zptlint file [files...]')  # noqa
        sys.exit(1)
    else:
        register('provider', TALESProviderExpression)
        register_addons()
        for arg in sys.argv[1:]:
            test(arg)


def register(name, handler):
    """Register tales expression type."""
    Engine.registerType(name, handler)


def register_addons():
    """Register additional expression types, if available."""
    try:
        from z3c.macro.tales import MacroExpression
    except ImportError:
        pass
    else:
        register('macro', MacroExpression)


def test(file):
    raw_data = open(file, 'r').read()
    pt = PageTemplate()
    pt.write(raw_data)
    if pt._v_errors:
        print('*** Error in:', file)  # noqa
        for error in pt._v_errors[1:]:
            formatted = error.replace('\n', ' ')
            linepos = formatted.rfind(', at line')
            if linepos != -1:
                formatted, formatted2 = (
                    formatted[:linepos], formatted[linepos:])
            else:
                formatted2 = ''
            print('    ', formatted)  # noqa
            print('    ', formatted2)  # noqa
        print()  # noqa
