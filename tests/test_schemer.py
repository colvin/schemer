#!/usr/bin/env python
#
# $Id$

from importlib.machinery import SourceFileLoader
from types import ModuleType
import json
from hashlib import md5
import pytest

loader = SourceFileLoader('schemer', 'schemer')
schemer = ModuleType(loader.name)
loader.exec_module(schemer)

pytest.schemer_data_prefix = 'tests/schemer'

def core_assertions(inst):
    assert inst
    assert isinstance(inst, schemer.Schemer)
    assert 'mode' in inst.__dict__
    assert isinstance(inst.mode, str)
    assert 'output_file' in inst.__dict__
    assert 'output_fh' in inst.__dict__
    assert 'output_buffer' in inst.__dict__
    assert 'order' in inst.__dict__
    assert isinstance(inst.order, list)
    assert 'macros' in inst.__dict__
    assert isinstance(inst.macros, dict)

def test_one():
    expected_order = [
        '/'.join([pytest.schemer_data_prefix, 'PROLOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'three/PROLOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'three/A.sql']),
        '/'.join([pytest.schemer_data_prefix, 'three/B.sql']),
        '/'.join([pytest.schemer_data_prefix, 'three/EPILOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'one/PROLOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'one/D.sql']),
        '/'.join([pytest.schemer_data_prefix, 'one/B.sql']),
        '/'.join([pytest.schemer_data_prefix, 'one/A.sql']),
        '/'.join([pytest.schemer_data_prefix, 'one/C.sql']),
        '/'.join([pytest.schemer_data_prefix, 'two/PROLOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'two/B.sql']),
        '/'.join([pytest.schemer_data_prefix, 'two/A.sql']),
        '/'.join([pytest.schemer_data_prefix, 'two/C.sql']),
        '/'.join([pytest.schemer_data_prefix, 'two/EPILOGUE.sql']),
        '/'.join([pytest.schemer_data_prefix, 'EPILOGUE.sql']),
    ]

    test_string = 'sd MACRO{SCHEMA_ONE}.abc MACRO{TEST_USER} asldkj MACRO{SCHEMA_THREE}dklsfjsa'
    expected_string = 'sd lemon.abc leroy asldkj snarfdklsfjsa'

    expected_digest = '5a5b331fc037c04d63525c9d1060e5d0'

    s = schemer.Schemer(pytest.schemer_data_prefix,
            macro_files=['/'.join([pytest.schemer_data_prefix, 'MACROS1'])],
            mode='buffer')
    core_assertions(s)
    assert s.mode == 'buffer'
    assert json.dumps(s.order) == json.dumps(expected_order)
    assert len(s.macros) == 5
    assert 'TEST_USER' in s.macros
    assert s.macros['TEST_USER'] == 'leroy'
    assert 'TEST_PASSWORD' in s.macros
    assert s.macros['TEST_PASSWORD'] == 'jenkins'
    assert 'SCHEMA_ONE' in s.macros
    assert s.macros['SCHEMA_ONE'] == 'lemon'
    assert 'SCHEMA_TWO' in s.macros
    assert s.macros['SCHEMA_TWO'] == 'lime'
    assert 'SCHEMA_THREE' in s.macros
    assert s.macros['SCHEMA_THREE'] == 'snarf'
    s.add_macros({'SCHEMA_ONE': 'coconut'})
    assert 'SCHEMA_ONE' in s.macros
    assert s.macros['SCHEMA_ONE'] == 'coconut'
    s.add_macros({'SCHEMA_ONE': 'lemon'})
    assert 'SCHEMA_ONE' in s.macros
    assert s.macros['SCHEMA_ONE'] == 'lemon'
    assert s.process_line(test_string) == expected_string

    s.run()

    assert s.output_buffer
    m = md5()
    for l in s.output_buffer:
        m.update(bytes(l, 'utf8'))
    assert m.hexdigest() == expected_digest

def test_two():
    expected_digest = '8f76509cbd97949ba3a64b6352639612'

    s = schemer.Schemer(pytest.schemer_data_prefix,
            macro_files=['/'.join([pytest.schemer_data_prefix, 'MACROS2'])],
            mode='buffer')

    core_assertions(s)
    assert 'TEST_USER' in s.macros
    assert s.macros['TEST_USER'] == '28374932874932'
    assert 'TEST_PASSWORD' in s.macros
    assert s.macros['TEST_PASSWORD'] == 'foo_bar'
    assert 'SCHEMA_ONE' in s.macros
    assert s.macros['SCHEMA_ONE'] == 'payload'
    assert 'SCHEMA_TWO' in s.macros
    assert s.macros['SCHEMA_TWO'] == 'dot'
    assert 'SCHEMA_THREE' in s.macros
    assert s.macros['SCHEMA_THREE'] == 'fart'

    s.run()

    assert s.output_buffer
    m = md5()
    for l in s.output_buffer:
        m.update(bytes(l, 'utf8'))
    assert m.hexdigest() == expected_digest
