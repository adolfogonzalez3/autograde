"""Module that contains functions for building and/or compiling programs."""

import subprocess
from pathlib import Path
from os import PathLike
from autograde.components.program import Program
from autograde.components.cpp_components import CppProgram
from autograde.tools.result import CompileResult, Result
from typing import Optional


def create_scons(program: Program, target_dir: PathLike) -> Path:
    """Returns a path a newly created scons file for a target program.

    args:
        program: A program to create a scons file for.
    """
    target_dir = Path(target_dir)
    construct_path = target_dir / 'SConstruct'
    with construct_path.open('wt') as construct:
        other_sources = program.source_files - {program.entry_point}
        dependencies = ", ".join(
            f"r'{sf.path.resolve()}'" for sf in other_sources
        )
        construct.write("\n".join(
            "Object("
            f"target = r'{target_dir / sf.path.name}'"
            f"source = r'{sf.path.resolve()}')"
            for sf in other_sources
        ))
        if program.entry_point is not None:
            absolute_path = program.entry_point.path.resolve()
            executable_path = target_dir / absolute_path.name
            construct.write(
                f"Program(r'{executable_path.with_suffix('.exe')}',"
                f"[r'{str(absolute_path)}', {dependencies}])"
            )
    return construct_path


def compile_cpp(
        program: CppProgram, target_path: PathLike) -> CompileResult:
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
    target_path = Path(target_path).resolve()
    executable: Optional[Path] = None
    if program.entry_point is not None:
        executable = target_path / program.entry_point.path.resolve()
        executable = executable.with_suffix(".exe")
    create_scons(program, target_path)
    proc_status = subprocess.run(
        ['scons'], shell=True, cwd=target_path, capture_output=True, text=True
    )
    if proc_status.returncode != 0:
        executable = None
    return CompileResult(
        executable, proc_status.stdout, proc_status.stderr,
        proc_status.returncode)


def clean_cpp(target_path: PathLike):
    """Cleans the target path of build files.

    args:
        target_path: The path to clean of build files.
    """
    proc_status = subprocess.run(
        ['scons', '-c'], shell=True, cwd=target_path, capture_output=True,
        text=True
    )
    return Result(
        proc_status.stdout, proc_status.stderr, proc_status.returncode
    )
