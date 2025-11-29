"""File handler for structured and unstructured outputs.

This module provides file handling functionality for structured and
unstructured outputs that the Claude Agent SDK doesn't have.
"""

import logging
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Any

from ..structure_converter import read_structure_from_filesystem

logger = logging.getLogger(__name__)


def create_structured_output_path() -> str:
    """
    Create a unique temporary directory path for storing structured output.

    Returns:
        str: Path string of a secure temporary directory
    """
    # Use tempfile.mkdtemp for secure temporary directory creation
    temp_dir = tempfile.mkdtemp(prefix="claude_data_structure_")
    logger.debug("Created secure temp directory: %s", temp_dir)
    return temp_dir


def create_unstructured_output_path() -> str:
    """
    Generate a unique temporary file path for unstructured output.

    Returns:
        A path string for a secure temporary unstructured output file.
    """
    # Use tempfile.mkstemp for secure temporary file creation
    fd, temp_path = tempfile.mkstemp(
        prefix="claude_unstructured_output_",
        suffix=".txt"
    )
    # Close the file descriptor since we just need the path
    os.close(fd)
    logger.debug("Created secure temp file: %s", temp_path)
    return temp_path


def read_structured_output(
    schema: dict[str, Any],
    output_dir: str,
) -> dict[str, Any]:
    """
    Assemble a dictionary by reading files in output_dir according to the provided schema.

    Parameters:
        schema (dict[str, Any]): JSON schema describing the expected file/folder structure and types.
        output_dir (str): Path to the directory containing the files and/or subdirectories that represent the structured output.

    Returns:
        dict[str, Any]: The assembled data matching the schema.

    Raises:
        RuntimeError: If the output directory does not exist.
    """
    output_path = Path(output_dir)

    if not output_path.exists():
        raise RuntimeError(
            f"Structured output directory not found: {output_dir}\n"
            f"Claude should have created this directory with the expected structure."
        )

    return read_structure_from_filesystem(schema, output_path)


def read_unstructured_output(output_file: str) -> str:
    """
    Read unstructured output from the given file.
    
    Parameters:
        output_file (str): Path to the unstructured output file.
    
    Returns:
        The file's contents as a string.
    
    Raises:
        RuntimeError: If the file does not exist.
    """
    output_path = Path(output_file)

    if not output_path.exists():
        raise RuntimeError(
            f"Unstructured output file not found: {output_file}\n"
            f"Claude should have created this file with the output."
        )

    content = output_path.read_text()
    logger.debug("Read %d characters from unstructured output file", len(content))

    return content


def cleanup_output_file(output_path: str) -> None:
    """
    Remove a temporary file or directory at the given path.

    If the path refers to a directory, it is removed recursively; if it refers to a file, the file is deleted. Any errors encountered during cleanup are logged and not raised.

    Parameters:
        output_path (str): Path to the temporary file or directory to remove.
    """
    path = Path(output_path)
    try:
        if path.is_dir():
            shutil.rmtree(path)
            logger.debug("Cleaned up output directory: %s", output_path)
        elif path.exists():
            path.unlink()
            logger.debug("Cleaned up output file: %s", output_path)
    except Exception as e:
        logger.warning("Failed to clean up output at %s: %s", output_path, e)