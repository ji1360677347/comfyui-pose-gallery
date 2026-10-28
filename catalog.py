"""Local, allow-listed pose catalogue. No runtime network downloads."""
import json
import os
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIBRARY = Path(os.environ.get('COMFYUI_POSE_GALLERY_LIBRARY', ROOT / 'library')).resolve()

@lru_cache(maxsize=1)
def records():
    source = LIBRARY / 'data' / 'pose-zh.json'
    if not source.is_file():
        raise FileNotFoundError('姿势图库尚未安装，请运行 python scripts/install_library.py')
    return json.loads(source.read_text(encoding='utf-8'))

@lru_cache(maxsize=1)
def index():
    return {row['id']: row for row in records()}

def pose(pose_id):
    try:
        return index()[pose_id]
    except KeyError:
        raise ValueError(f'未知姿势 ID：{pose_id}') from None

def asset(kind, filename):
    if kind not in ('img', 'thumbs') or Path(filename).name != filename or '\\' in filename:
        raise ValueError('无效图片路径')
    pose_id, suffix = os.path.splitext(filename)
    row = pose(pose_id)
    expected = row['原图' if kind == 'img' else '缩略图']
    relative = Path(kind) / filename
    target = (LIBRARY / relative).resolve()
    if expected != relative.as_posix() or not target.is_relative_to(LIBRARY):
        raise ValueError('图片不在图库中')
    if not target.is_file():
        raise FileNotFoundError(f'图片缺失：{relative}，请重新安装图库')
    return target
