"""A module that contains functions used throughout the testing env."""
from pathlib import Path
from itertools import product, chain
from typing import Tuple, Iterator, Any, List

import pytest


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
