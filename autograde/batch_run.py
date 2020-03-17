"""A script for running the autograder."""
import argparse
from os import PathLike
from pathlib import Path
from typing import List, Optional, Tuple, Iterator
from concurrent.futures import ProcessPoolExecutor
from time import time

from autograde import CppProgram
from autograde.components import Program
from autograde.tools import compile_cpp, execute_program, clean_cpp
from autograde.tools.container import compile_run_cpp
from autograde.tools.result import CompileResult, ExecuteResult

from tqdm import tqdm

RunResult = Tuple[Program, Optional[CompileResult], Optional[ExecuteResult]]


def get_args():
    """Gets command line arguments for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "program_path", help="Path to the programs to compile and run.",
        type=Path)
    parser.add_argument(
        "--program_input", help="Input fed into the program.",
        default=None, type=lambda x: x.replace("\\n", "\n"))
    parser.add_argument(
        "--use_container", action="store_true",
        help="Use a container to compile and run the program.")
    parser.add_argument(
        "--concurrent", action="store_true",
        help="Run each program's compilation and execution concurrently.")
    return parser.parse_args()


def run_program(
        program_path: PathLike, program_input: Optional[str] = None,
        use_container: bool = False) -> RunResult:
    """Runs a program contained in the path.

    args:
        program_path: A path that contains the program to compile and run.
        program_input: Input to give the program.
    returns:
        Returns the results of the compile and execution of the program.
    """
    program = CppProgram(program_path)
    program.collect_source()
    program.set_entry_point()
    if use_container:
        compile_result, execute_result = compile_run_cpp(
            program, program_input=program_input)
    else:
        clean_cpp(program_path)
        compile_result = compile_cpp(program, target_path=program_path)
        execute_result = None
        if compile_result and compile_result.executable is not None:
            execute_result = execute_program(
                compile_result.executable, compile_result.executable.parent,
                program_input=program_input
            )
    return (program, compile_result, execute_result)


def batch_run_programs(
        batch_path: PathLike, program_input: Optional[str] = None,
        use_container: bool = False, concurrent: bool = False
) -> Iterator[Tuple[Path, RunResult]]:
    """Runs multiple programs in a folder within a folder.

    args:
        batch_path: The path to a directory that contains subdirectories that
            contains program code.
        program_input: Input to give to the program.
    returns:
        Returns the results of the compilation process and the execution
            process.
    """
    program_folders = list(Path(batch_path).iterdir())
    if concurrent:
        with ProcessPoolExecutor() as executor:
            tasks = executor.map(
                run_program, program_folders,
                [program_input]*len(program_folders),
                [use_container]*len(program_folders)
            )
            yield from zip(program_folders, tasks)
    else:
        yield from (
            (
                program_path,
                run_program(program_path, program_input, use_container)
            )
            for program_path in program_folders
        )


def display(results: List[Tuple[Path, RunResult]]):
    """Displays the results of compiling and running the programs.

    args:
        program_results: The results from compiling and running multiple
            programs.
    """
    print("-"*80)
    for prog_path, (program, compile_result, execute_result) in results:
        print("Path:", prog_path)
        print("Entry Point:", program.entry_point)
        if compile_result is not None:
            print("Compiling...")
            print("STDOUT")
            print(compile_result.stdout)
            print("STDERR")
            print(compile_result.stderr)
        if execute_result is not None:
            print("Executing...")
            print("STDOUT:")
            print(execute_result.stdout)
            print("STDERR")
            print(execute_result.stderr)
        # for source_file in program.source_files:
        #    print(source_file.functions)
        print("*"*80)
    print("-"*80)


def main():
    args = get_args()
    with tqdm(batch_run_programs(
            args.program_path, program_input=args.program_input,
            use_container=args.use_container, concurrent=args.concurrent
    )) as batches:
        program_results = list(batches)
    display(program_results)


if __name__ == "__main__":
    begin = time()
    main()
    print("Time Elapsed: ", time() - begin)
