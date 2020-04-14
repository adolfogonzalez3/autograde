"""Module which contains the components that represent a cpp program."""

import re
from os import PathLike
from typing import List, Tuple, Union, Optional

from autograde.components.program import Program, Source


def get_functions(source_code: str) -> List[Tuple[str, str, Tuple[str, ...]]]:
    """Gets the functions from source code.

    args:
        source_code: Source code that is compliant with C++ standard.
    returns:
        A list of functions extracted from the source code.
    """
    function_pattern = re.compile(
        r'([a-z|A-Z][a-z|A-Z|0-9|_|<|>|\*]+?)\s+' # Represents the return type
        r'([a-z|A-Z][a-z|A-Z|0-9|_]*?)\s*'  # Represents the function name
        r'\((.*?)\)'  # represents the function arguments
        r'\s*{.*?}',  # Represents the body of the function
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
