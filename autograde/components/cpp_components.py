"""Module which contains the components that represent a cpp program."""

import re
from os import PathLike
from typing import List, Tuple, Union, Optional
import subprocess

from autograde.components import Program, Source


def get_functions(source_code: str) -> List[Tuple[str, str, Tuple[str, ...]]]:
    """Gets the functions from source code.

    args:
        source_code: Source code that is compliant with C++ standard.
    returns:
        A list of functions extracted from the source code.
    """
    function_pattern = re.compile(
        r'([a-z|A-Z|0-9|_|<|>|\*]+?)\s+?'  # Represents the return type
        r'(\w+?)'  # Represents the function name
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

    def __init__(self, root_path, path_to_entry_point=None):
        super().__init__(root_path, path_to_entry_point)
        for source_file in self.source_files:
            if source_file.is_entry_point():
                self.entry_point = source_file

    def get_extensions(self):
        """See base class."""
        return ('.cpp', '.h')

    @property
    def source_type(self):
        """See base class."""
        return CppSource

    def check(self):
        """See base class."""
        results = []
        main_pattern = re.compile(r'int\s+main')
        header_pattern = re.compile(
            # r'/\*+.?\s+'
            r'//\s*class:\s*.+?\s+'
            r'//\s*section:\s*.+?\s+'
            r'//\s*semester:\s*.+?\s+'
            r'//\s*lab:\s*.+?\s+'
            r'(//\s*name:\s*.+?\s+)+'
            # r'.?\*+/'
        )
        for file_path in self.source_files:
            has_main_flag = False
            with file_path.open('rt') as source_stream:
                source_code = ' '.join(line for line in source_stream)
            if main_pattern.search(source_code):
                has_main_flag = True
            header = header_pattern.search(source_code.lower())
            if header and self.header is None:
                self.header = header
            results.append(
                CheckTuple(file_path, has_main_flag)
            )
        return results

    def compile(self, args=None, kwargs=None):
        """See base class."""
        with (self.root_path / 'SConstruct').open('wt') as construct:
            construct.write(
                f"Program(r'{str(self.entry_point.path)}')"
            )
        subprocess.run(
            ['scons'], shell=True, cwd=self.root_path, capture_output=True
        )

    def clean(self):
        """See base class."""


    def execute(self, args=None, kwargs=None):
        """See base class."""
        return
