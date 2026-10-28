#!/usr/bin/env python3
"""Download the user-selected upstream library separately from the node code."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/wangweihong/ai-pose-gallery-zh.git'

def install(source, destination):
    rows = json.loads((source / 'data/pose-zh.json').read_text())
    for row in rows:
        for field in ('原图', '缩略图'):
            file = (source / row[field]).resolve()
            if not file.is_relative_to(source.resolve()) or not file.is_file():
                raise ValueError(f'图库不完整或路径无效：{row[field]}')
    destination.mkdir(parents=True, exist_ok=True)
    for name in ('data', 'img', 'thumbs'):
        shutil.copytree(source / name, destination / name, dirs_exist_ok=True)
    for name in ('LICENSE', 'README.md'):
        shutil.copy2(source / name, destination / name)
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    (destination / 'SOURCE.json').write_text(json.dumps({'url': REPO, 'revision': revision, 'images': len(rows)}, indent=2))
    print(f'已安装 {len(rows)} 张原图、{len(rows)} 张缩略图：{destination}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='已有的 ai-pose-gallery-zh clone')
    parser.add_argument('--destination', type=Path, default=ROOT / 'library')
    args = parser.parse_args()
    if args.source:
        install(args.source.resolve(), args.destination)
    else:
        with tempfile.TemporaryDirectory(prefix='pose-gallery-') as tmp:
            source = Path(tmp) / 'upstream'
            subprocess.run(['git', 'clone', '--depth', '1', REPO, str(source)], check=True)
            install(source, args.destination)
