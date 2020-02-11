"""A script for running the autograder."""
import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from autograde import CppProgram

def get_args():
    """Gets command line arguments for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_to_assn', help='Path to the assignments.', type=Path)
    return parser.parse_args()

def main():
    args = get_args()
    assn_path = args.path_to_assn
    with ProcessPoolExecutor() as executor:
        students = [
            (student_path, CppProgram(student_path))
            for student_path in assn_path.iterdir()
        ]
        # print(students)
        #for name, student in students:
        if True:
            name, student = students[0]
            result = student.compile()
            print('*'*80)
            print(f'Student: {name}')
            if result:
                print("Executing...")
                print(student.execute())
            #if student.header:
            #    print("EXISTS")
            #else:
            #    print("NOTHING")
            #if result:
            #    print(result.stdout.decode())
            #else:
            #    print("NOTHING")
            print('*'*80)
        # responses = executor.map(compile_and_run, students,
        #                         [trials] * len(students))
    #responses, students, grades = zip(*list(responses))
    # for student, grade in zip(students, grades):
    #    print(f'{student} {sum(grade)} correct out of {len(grade)}')

    # with open(args.output, 'wt') as log:
    #    json.dump(responses, log, indent=4)

if __name__ == "__main__":
    main()
