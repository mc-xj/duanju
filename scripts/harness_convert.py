"""Use Harness Anything's existing LibreOffice backend for local file conversion."""
import argparse
from pathlib import Path
from cli_anything.office.utils.office_backend import convert_to

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
if not args.output.suffix:
    parser.error("Output must have a file extension, for example .pdf")
print(convert_to(str(args.source), args.output.suffix[1:], str(args.output), overwrite=False))
