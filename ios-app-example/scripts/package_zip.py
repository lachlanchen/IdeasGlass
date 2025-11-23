#!/usr/bin/env python3
import argparse
import shutil
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description='Zip a file or folder into dist/')
parser.add_argument('source', help='File or directory to zip')
parser.add_argument('--name', default='firmware.zip', help='Output zip name (default firmware.zip)')
parser.add_argument('--dist', default='dist', help='Output directory (default dist)')
args = parser.parse_args()

src = Path(args.source).expanduser().resolve()
if not src.exists():
    raise SystemExit(f'source not found: {src}')

dist = Path(args.dist).resolve()

dist.mkdir(parents=True, exist_ok=True)
base = dist / Path(args.name).stem

if src.is_file():
    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        shutil.copy2(src, tmpdir / src.name)
        archive = shutil.make_archive(str(base), 'zip', str(tmpdir))
else:
    archive = shutil.make_archive(str(base), 'zip', str(src))

print(archive)
