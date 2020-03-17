"""A script for running the autograder."""

import argparse
from time import time
from pathlib import Path

from autograde.batch_run import run_program, display


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
    return parser.parse_args()


def main():
    args = get_args()
    program_results = run_program(
        args.program_path, program_input=args.program_input,
        use_container=args.use_container
    )
    display([(args.program_path, program_results)])


if __name__ == "__main__":
    begin = time()
    main()
    print("Time Elapsed: ", time() - begin)
