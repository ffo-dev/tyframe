from pathlib import Path


def compare_with_expected(
    generated: str,
    expected_path: Path,
) -> None:
    """Compare generated code with expected file, ignoring empty lines.

    Args:
        generated: The generated code string.
        expected_path: Path to the expected output file.

    Raises:
        AssertionError: If the generated and expected content don't match.
    """
    expected = expected_path.read_text()

    # Strip and split by lines, filtering out empty lines
    generated_lines = [line for line in generated.strip().split('\n') if line.strip()]
    expected_lines = [line for line in expected.strip().split('\n') if line.strip()]

    # Compare line by line
    assert generated_lines == expected_lines, (
        f'Generated code does not match expected.\nGenerated:\n{generated}\nExpected:\n{expected}'
    )
