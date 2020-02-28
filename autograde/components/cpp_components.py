"""Module which contains the components that represent a cpp program."""

import re
from os import PathLike
from typing import List, Tuple, Union, Optional
import subprocess

from autograde.components import Program, Source
from autograde.tools.result import Result


def get_functions(source_code: str) -> List[Tuple[str, str, Tuple[str, ...]]]:
    """Gets the functions from source code.

    args:
        source_code: Source code that is compliant with C++ standard.
    returns:
        A list of functions extracted from the source code.
    """
    function_pattern = re.compile(
        r'([a-z|A-Z|0-9|_|<|>|\*]+?)\s+?'  # Represents the return type
        r'(\w+?)\s*'  # Represents the function name
        r'\(\s*(.*?)\s*\)'  # represents the function arguments
        r'\s*?{.*?}',  # Represents the body of the function
        flags=re.DOTALL
    )
    functions = []
    for match in function_pattern.finditer(source_code):
        return_type, name, args = match.group(1, 2, 3)
        args_tuple: Tuple[str, ...] = tuple(
            [arg.strip() for arg in args.split(',') if arg]
        )
        functions.append((return_type, name, args_tuple))
    return functions


def get_comments(source_code: str) -> List[str]:
    """Gets the comments from the source code.

    args:
        source_code: Source code that is compliant with C++ standard.
    returns:
        A list for comments extracted from the source code.
    """
    comment_pattern = re.compile(
        r'(//.*?\n|/\*.*?\*/)',
        flags=re.DOTALL
    )
    comments = [
        match.group(0).strip()
        for match in comment_pattern.finditer(source_code)
    ]
    return comments


class CppSource(Source):
    """Represents the source code for a C++ file.

    attributes:
        _functions: A sequence of tuples which contain the function signatures
            for the source code.
        _comments: A sequence of comments extracted from the source code.
    """

    def __init__(self, *path_to_source: Union[str, PathLike]):
        super().__init__(*path_to_source)
        self._functions: Optional[Tuple[str, str, Tuple[str, ...]]] = None
        self._comments: Optional[Tuple[str]] = None

    def load(self):
        """Reads the source file and extracts all the information needed."""
        with self.path.open('rt') as cpp_source:
            code = ''.join(cpp_source)
            self._functions = tuple(get_functions(code))
            self._comments = tuple(get_comments(code))

    @property
    def functions(self):
        """See base class."""
        if self._functions is None:
            self.load()
        return self._functions

    @property
    def comments(self):
        """See base class."""
        if self._comments is None:
            self.load()
        return self._comments

    def is_entry_point(self) -> bool:
        """See base class."""
        for return_type, name, _ in self.functions:
            if return_type == 'int' and name == 'main':
                return True
        return False


class CppProgram(Program):
    """A representation of a C++ program."""

    def get_extensions(self):
        """See base class."""
        return ('.cpp', '.h')

    @property
    def source_type(self):
        """See base class."""
        return CppSource

    def compile(self, target_path) -> Result:
        """See base class."""
        if self.entry_point is None:
            return Result("", "", 1)
        if self.entry_point.path.with_suffix('.exe').exists():
            self.executable = self.entry_point.path.with_suffix('.exe')
            return Result("", "", 0)
        with (target_path / 'SConstruct').open('wt') as construct:
            absolute_path = self.entry_point.path.resolve()
            construct.write(
                f"Program(r'{absolute_path.with_suffix('.exe').name}',"
                f"r'{str(absolute_path)}')"
            )
        proc_status = subprocess.run(
            ['scons'], shell=True, cwd=target_path, capture_output=True
        )
        match = re.search(r"\s*/OUT:(\S+)\s*", proc_status.stdout.decode())
        if match is not None:
            self.executable = target_path / match.group(1)
        return Result(
            proc_status.stdout.decode(), proc_status.stderr.decode(),
            proc_status.returncode)

    def clean(self, target_path) -> Result:
        """See base class."""
        proc_status = subprocess.run(
            ['scons', '--clean'], shell=True, cwd=target_path,
            capture_output=True
        )
        return Result(
            proc_status.stdout, proc_status.stderr, proc_status.returncode)

    def execute(self, proc_input: Optional[str] = None) -> Result:
        """See base class."""
        if self.executable is None:
            self.compile()
            if self.executable is None:
                return Result("", "", 1)
        proc_status = subprocess.run(
            [str(self.executable.resolve())],
            cwd=self.root_path, capture_output=True,
            input=proc_input, text=True
        )
        return Result(
            proc_status.stdout, proc_status.stderr,
            proc_status.returncode)
