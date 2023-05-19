"""
This module validates and parses the provided command-line arguments.
"""
import argparse
from pathlib import Path


def check_positive(value: str):
    """
    Validates whether width and height command-line arguments are digits and greater 0.

    Args:
        value: Value to validate

    Returns:
        Integer of input if input is validated

    Raises:
        argpass.ArgumentTypeError: Input is not a digit or smaller than 1.
    """
    if not value.isdigit():
        raise argparse.ArgumentTypeError(
            f"Invalid datatype {type(value)}: expected positive Integer.")
    if int(value) < 1:
        raise argparse.ArgumentTypeError(f"Value {value} is less than 1.")
    return int(value)


def check_output_destination(path: str):
    """
    Validates if output file:
        -   is in a parent folder that exists
        -   is not a directory
        -   does not yet exist
        -   is either .jpg or png

    Args:
        path: Path to validate

    Returns:
        Path if is successfully validated

    Raises:
        argpass.ArgumentTypeError: Path does not follow constraints
    """
    valid_path = Path(path)
    if not valid_path.parent.exists():
        raise argparse.ArgumentTypeError(
            f"The folder '{valid_path.parent}' does not exist.")
    if valid_path.is_dir():
        raise argparse.ArgumentTypeError("Please specify filename")
    if valid_path.exists():
        raise argparse.ArgumentTypeError(
            f"The file '{valid_path.name}' already exists")
    if valid_path.suffix not in ['.png', '.jpg']:
        raise argparse.ArgumentTypeError(
            "The output file has to be either .JPG or .PNG")
    return path


parser = argparse.ArgumentParser()

parser.add_argument('input', metavar='input_destination',
                    type=argparse.FileType('r', encoding='utf-8'),
                    help='Path to an image used for transformation')
parser.add_argument('output', metavar='output_destination',
                    type=check_output_destination,
                    help='Path to output file')
parser.add_argument('width', metavar='output_width',
                    type=check_positive,
                    help='Desired width of output image')
parser.add_argument('height', metavar='output_height',
                    type=check_positive,
                    help='Desired height of output image')
