"""Module that contains functions for building and/or compiling programs."""

import subprocess
from pathlib import Path
from os import PathLike
from autograde.components.cpp_components import CppProgram
from autograde.tools.result import CompileResult
from typing import List, Tuple, Union, Optional


def compile_cpp(
        program: CppProgram, target_path: PathLike) -> Optional[CompileResult]:
    """Compile a cpp program using the system's compiler.

    Compiles a C++ program using the system's compiler. The compiler is found
    by SCONS. The entry point is used to name the executable.

    args:
        program: Represents the program which you want to compile. Should
            have an entry point.
        target_path: The path to store the final executable.

    Returns:
        A CompileResult Namedtuple which consists of the path to the
            executable, output from stdout, output from stderr, and the
            return code.
    """
    target_path = Path(target_path)
    if program.entry_point is None:
        return None
    executable = target_path / program.entry_point.path.with_suffix('.exe')
    with (target_path / 'SConstruct').open('wt') as construct:
        absolute_path = program.entry_point.path.resolve()
        other_sources = program.source_files - {program.entry_point}
        dependencies = ", ".join(
            f"r'{sf.path.resolve()}'" for sf in other_sources
        )
        construct.write(
            f"Program(r'{absolute_path.with_suffix('.exe').name}',"
            f"[r'{str(absolute_path)}', {dependencies}])"
        )
    proc_status = subprocess.run(
        ['scons'], shell=True, cwd=target_path, capture_output=True, text=True
    )
    return CompileResult(
        executable, proc_status.stdout, proc_status.stderr,
        proc_status.returncode)


def clean_cpp(target_path: PathLike):
    """Cleans the target path of build files.

    args:
        target_path: The path to clean of build files.
    """
    subprocess.run(
        ['scons', 'clean'], shell=True, cwd=target_path, capture_output=True
    )
