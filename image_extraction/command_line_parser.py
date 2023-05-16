import argparse
from pathlib import Path

def check_positive(value: str):
    if not value.isdigit():
        raise argparse.ArgumentTypeError(f"Invalid datatype {type(value)}: expected positive Integer.")
    if int(value) < 1:
        raise argparse.ArgumentTypeError(f"Value {value} is less than 1.")
    return int(value)

def check_output_destination(path: str):
    valid_path = Path(path)
    if not valid_path.parent.exists():
        raise argparse.ArgumentTypeError(f"The folder '{valid_path.parent}' does not exist.")
    if valid_path.is_dir():
        raise argparse.ArgumentTypeError("Please specify filename")
    if valid_path.exists():
        raise argparse.ArgumentTypeError(f"The file '{valid_path.name}' already exists")
    # TODO: check file ending
    return path

parser = argparse.ArgumentParser()

parser.add_argument('input', metavar='input_destination',
                    type=argparse.FileType('r', encoding='utf-8'),
                    help='Path to a picture used for transformation')
parser.add_argument('output', metavar='output_destination',
                    type=check_output_destination,
                    help='Path to a picture used for transformation')
parser.add_argument('width', metavar='output_width',
                    type=check_positive,
                    help='Desired width of output image')
parser.add_argument('height', metavar='output_height',
                    type=check_positive,
                    help='Desired height of output image')
