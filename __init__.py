"""comfyui-pose-gallery: browse local pose references and output an IMAGE."""
import hashlib
import json
import numpy as np
import torch
from PIL import Image, ImageOps
from aiohttp import web
from server import PromptServer
from .catalog import records, pose, asset, ROOT

class PoseGallery:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'pose_id': ('STRING', {'default': 'full_sexy_P031_front', 'multiline': False, 'tooltip': '点击浏览姿势图库，选择视角后使用；也可以直接输入图库 ID。'})}}

    RETURN_TYPES = ('IMAGE', 'INT', 'INT', 'STRING', 'STRING')
    RETURN_NAMES = ('image', 'width', 'height', 'pose_id', 'description')
    FUNCTION = 'load_pose'
    CATEGORY = 'image/Pose Gallery'
    DESCRIPTION = '本地中文姿势图库：搜索、体系/动作/角度筛选、分组浏览、多视角预览。选择原图输出到 Depth Anything。'

    @classmethod
    def VALIDATE_INPUTS(cls, pose_id):
        try:
            row = pose(pose_id)
            asset('img', row['原图'].split('/')[-1])
        except (ValueError, FileNotFoundError) as exc:
            return str(exc)
        return True

    @classmethod
    def IS_CHANGED(cls, pose_id):
        row = pose(pose_id)
        return hashlib.sha256(asset('img', row['原图'].split('/')[-1]).read_bytes()).hexdigest()

    def load_pose(self, pose_id):
        row = pose(pose_id)
        with Image.open(asset('img', row['原图'].split('/')[-1])) as source:
            img = ImageOps.exif_transpose(source).convert('RGBA')
            background = Image.new('RGBA', img.size, 'white')
            img = Image.alpha_composite(background, img).convert('RGB')
            width, height = img.size
            tensor = torch.from_numpy(np.asarray(img).astype(np.float32) / 255.0).unsqueeze(0)
        description = ' / '.join(row.get(k, '') for k in ('体系', '分类', '姿势名称', '角度'))
        return (tensor, width, height, pose_id, description)

routes = PromptServer.instance.routes

@routes.get('/pose_gallery/catalog')
async def catalog_route(request):
    try:
        return web.json_response(records())
    except (ValueError, FileNotFoundError) as exc:
        return web.json_response({'error': str(exc)}, status=503)

@routes.get('/pose_gallery/assets/{kind}/{filename}')
async def asset_route(request):
    try:
        path = asset(request.match_info['kind'], request.match_info['filename'])
        return web.FileResponse(path, headers={'Cache-Control': 'private, max-age=3600'})
    except (ValueError, FileNotFoundError):
        raise web.HTTPNotFound()

@routes.get('/pose_gallery/gallery')
async def gallery_route(request):
    return web.FileResponse(ROOT / 'web' / 'gallery.html', headers={'Cache-Control': 'no-cache'})

NODE_CLASS_MAPPINGS = {'PoseGallery': PoseGallery}
NODE_DISPLAY_NAME_MAPPINGS = {'PoseGallery': 'Pose Gallery 姿势图库'}
WEB_DIRECTORY = './web'
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
