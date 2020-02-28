"""Tests the build module's functions."""

from pathlib import Path

import autograde.components as components
import autograde.tools.build as build_tools


def test_compile_cpp(tmp_path, simple_program):
    """Tests CppProgram compile method."""
    cpp_program = components.CppProgram(tmp_path)
    cpp_program.collect_source()
    cpp_program.set_entry_point()
    result = build_tools.compile_cpp(cpp_program, target_path=tmp_path)
    for path in Path(tmp_path).iterdir():
        print(path)
    for source in cpp_program.source_files:
        print(source)
    assert result is not None
    assert result[0].exists()
    assert bool(result)


def ttest_cpp_program_clean(tmp_path, simple_program):
    """Tests CppProgram clean method."""
    tmp_path = Path(tmp_path)
    cpp_program = components.CppProgram(tmp_path)
    cpp_program.collect_source()
    cpp_program.set_entry_point()
    build_tools.compile_cpp(cpp_program, target_path=tmp_path)
    for path in tmp_path.iterdir():
        print(path)
    for source in cpp_program.source_files:
        print(source)
    assert not list(tmp_path.rglob('*.o'))
    assert not list(tmp_path.rglob('*.obj'))
