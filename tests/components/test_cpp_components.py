
from itertools import zip_longest

import autograde.components.cpp_components as components


def test_get_functions(simple_func_code):
    """Tests get_functions method."""
    code, funcs = simple_func_code
    for actual, result in zip_longest(funcs, components.get_functions(code)):
        print("a>", actual)
        print("r>", result)
        assert actual == result


def test_get_comments(simple_comment_code):
    """Tests get_comments method."""
    code, comments = simple_comment_code
    for actual, result in zip_longest(comments, components.get_comments(code)):
        print("a>", actual)
        print("r>", result)
        assert actual == result


def test_cpp_source_is_entry_point_entry_point(simple_program):
    """Tests CppSource is_entry_point method."""
    cpp_source = components.CppSource(simple_program)
    for signature in cpp_source.functions:
        print(signature)
    assert cpp_source.is_entry_point()


def test_cpp_source_is_entry_point_entry_point_cmdline(
        simple_program_with_cmdline_args):
    """Tests CppSource is_entry_point method."""
    cpp_source = components.CppSource(simple_program_with_cmdline_args)
    for signature in cpp_source.functions:
        print(signature)
    assert cpp_source.is_entry_point()


def test_cpp_source_is_entry_point_not_entry_point(
        simple_source):
    """Tests CppSource is_entry_point method."""
    cpp_source = components.CppSource(simple_source)
    for signature in cpp_source.functions:
        print(signature)
    assert not cpp_source.is_entry_point()


def test_cpp_program_collect(tmp_path, simple_source, simple_program):
    """Tests CppProgram collect method."""
    source_files = {
        components.CppSource(simple_source),
        components.CppSource(simple_program),
    }
    cpp_program = components.CppProgram(tmp_path)
    cpp_program.collect_source()
    cpp_program.set_entry_point()
    assert cpp_program.source_files == source_files
    assert cpp_program.entry_point == components.CppSource(simple_program)
