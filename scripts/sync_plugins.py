"""Generate native plugin skill snapshots from the canonical skills/ sources."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def files(folder):
    return {path.relative_to(folder): path.read_bytes() for path in folder.rglob('*')
            if path.is_file() and '__pycache__' not in path.parts}


def sync(root=ROOT, check=False):
    for source in sorted((root / 'skills').iterdir()):
        if not source.is_dir():
            continue
        target = root / 'plugins' / source.name / 'skills' / source.name
        if not (target.parent.parent / 'plugin.json').is_file():
            raise ValueError(f'{source.name}: missing plugin adapter')
        if check:
            if not target.parent.is_dir() or {path.name for path in target.parent.iterdir()} != {source.name}:
                raise ValueError(f'{source.name}: plugin must contain only its own skill')
            if files(source) != files(target):
                raise ValueError(f'{source.name}: stale plugin snapshot; run make plugins')
        else:
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    sync(check=parser.parse_args().check)
    print('Plugin snapshots match canonical skills.')
