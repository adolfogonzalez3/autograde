
from pathlib import Path
from itertools import product, chain, zip_longest
from typing import Tuple, Iterator, Any, List

import pytest

import autograde.components.cpp_components as components


def yield_func_code() -> Iterator[Tuple[str, Tuple[str, str, Tuple[str, ...]]]]:
    """Yields generated C++ code."""
    CPP_TYPES = ["int", "float"]
    for num_types in range(1, 5):
        for types in product(CPP_TYPES, repeat=num_types):
            return_type, *arg_types = types
            func_name = 'func_' + '_'.join(types)
            args = [f"{typ} a_{i}" for i, typ in enumerate(arg_types)]
            args_joined = ', '.join(args)
            yield (
                f"{return_type} {func_name}({args_joined}){{return 0;}}",
                (return_type, func_name, tuple(args))
            )


@pytest.fixture
def simple_func_code() -> Tuple[str, Tuple[Any, ...]]:
    """Produces some simple test code."""
    code, structure = zip(*list(yield_func_code()))
    return "\n".join(code), structure


@pytest.fixture
def simple_comment_code() -> Tuple[str, List[str]]:
    """Returns some commented code along with the strings in the comments."""
    single_line_comments = [
        '// comment_0 for C++',
        '//comment_1 for C++.',
        '///comment_2 for C++.',
    ]
    multi_line_comments = [
        '/*header\nnext line\n next next line\n*/',
        '/*\nthis\nis\na\ntest*/',
    ]
    code = '\n'.join(chain(single_line_comments, multi_line_comments))
    return code, single_line_comments + multi_line_comments


@pytest.fixture
def simple_program(tmp_path, simple_func_code) -> Path:
    """Returns a path to a source file with an entry point."""
    func_code, _ = simple_func_code
    program_code = f"{func_code}\nint main() {{\nreturn 0;\n}}\n"
    tmp_source_path = Path(tmp_path, 'simple_program.cpp')
    with tmp_source_path.open('wt') as src:
        src.write(program_code)
    return tmp_source_path


@pytest.fixture
def simple_program_with_cmdline_args(tmp_path, simple_func_code) -> Path:
    """Returns a path to a source file with an entry point."""
    func_code, _ = simple_func_code
    program_code = "\n".join([
        func_code, f"int main(int argc, char** argv) {{\nreturn 0;\n}}\n"
    ])
    tmp_source_path = Path(tmp_path, 'simple_program.cpp')
    with tmp_source_path.open('wt') as src:
        src.write(program_code)
    return tmp_source_path


@pytest.fixture
def simple_source(tmp_path, simple_func_code) -> Path:
    """Returns a path to a simple source file that isn't an entry point."""
    func_code, _ = simple_func_code
    tmp_source_path = Path(tmp_path, 'simple_source.cpp')
    with tmp_source_path.open('wt') as src:
        src.write(func_code)
    return tmp_source_path


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
    assert cpp_program.source_files == source_files
    assert cpp_program.entry_point == components.CppSource(simple_program)


def test_cpp_program_compile(tmp_path, simple_source, simple_program):
    """Tests CppProgram compile method."""
    cpp_program = components.CppProgram(tmp_path)
    cpp_program.compile()
    for path in Path(tmp_path).iterdir():
        print(path)
    assert cpp_program.executable is not None
    assert cpp_program.executable.exists()
