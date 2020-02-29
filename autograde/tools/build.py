"""Module that contains functions for building and/or compiling programs."""

import json
import shutil
import subprocess
from pathlib import Path
from os import PathLike
import autograde
from autograde.components.program import Program
from autograde.components.cpp_components import CppProgram
from autograde.tools.result import CompileResult, Result
from typing import Optional, Tuple


def create_scons(program: Program, target_dir: PathLike) -> Tuple[Path, Path]:
    """Returns a path a newly created scons file for a target program.

    args:
        program: A program to create a scons file for.
    """
    sconstruct_template = Path(autograde.__file__).parent
    sconstruct_template = sconstruct_template / "templates" / "SConstruct"
    target_dir = Path(target_dir)
    build_info_file = target_dir / 'build_info.json'
    other_sources = program.source_files - {program.entry_point}
    dependencies = ", ".join(str(sf.path.resolve()) for sf in other_sources)
    build_info = {
        "source_files": dependencies,
        "executable_path": None
    }
    if program.entry_point is not None:
        absolute_path = program.entry_point.path.resolve()
        executable_path = target_dir / absolute_path.name
        build_info["entry_point"] = str(absolute_path)
        build_info["executable_path"] = str(executable_path.with_suffix('.exe'))
    with build_info_file.open("wt") as bf:
        json.dump(build_info, bf)
    
    print(sconstruct_template, sconstruct_template.exists())
    shutil.copy(sconstruct_template, target_dir / sconstruct_template.name)
    return sconstruct_template, build_info_file


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
        executable = target_path / program.entry_point.path.name
        executable = executable.with_suffix(".exe")
    scons_path, info_file = create_scons(program, target_path)
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
