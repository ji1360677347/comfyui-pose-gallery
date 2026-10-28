# comfyui-pose-gallery

ComfyUI 本地中文姿势图库节点。参考并改编 [ai-pose-gallery-zh](https://github.com/wangweihong/ai-pose-gallery-zh) 的画廊界面：1,439 张原图，288 组姿势，最多 5 个视角。

## 使用

添加 **image → Pose Gallery → Pose Gallery 姿势图库**，点击“浏览姿势图库”，按中文关键词、编号或 ID 搜索，使用体系、动作和视角筛选。点卡片进入大图，切换视角，点击“使用此姿势 → ComfyUI”。所选 ID 会保存在节点及工作流中，节点显示当前原图。

输出：`image`（RGB，900×1200）、`width`、`height`、`pose_id`、`description`。输出 `image` 可连接 Depth Anything、图像预览及其他图像节点。不自动入队；用户点击 ComfyUI“运行”开始生成。

## 安装

在 `ComfyUI/custom_nodes` 目录执行：

```bash
git clone https://github.com/wangweihong/comfyui-pose-gallery.git
```

重启 ComfyUI 并刷新浏览器。仓库已直接包含 **1,439 张 JPG 缩略图和中文索引**，克隆后即可离线浏览、搜索和筛选图库，无需另外下载缩略图。

```text
comfyui-pose-gallery/
└── library/
    ├── data/       # 随仓库提供的中文姿势索引和分类
    ├── thumbs/     # 随仓库提供的 1,439 张缩略图
    └── SOURCE.json # 素材来源和版本
```

### 安装原尺寸图片（用于大图预览及生图）

缩略图为 300×400 JPG；节点向工作流输出的原图为 900×1200 PNG。**本仓库包含缩略图，原尺寸 PNG 仍需单独安装**。在节点目录使用 ComfyUI 所在环境的 Python 执行：

```bash
cd comfyui-pose-gallery
python scripts/install_library.py
```

脚本需要 Git，会从 [wangweihong/ai-pose-gallery-zh](https://github.com/wangweihong/ai-pose-gallery-zh) 获取完整图库，约 660 MB，并将原图安装到 `library/img/`。已有完整图库 Git clone 时，也可直接复制安装：

```bash
python scripts/install_library.py --source /path/to/ai-pose-gallery-zh
```

安装完成后，浏览姿势和向工作流加载原图均使用本地文件。已经安装完整素材的环境无需重复下载；本项目实测的本地 ComfyUI 环境已有全部原图和缩略图。若提示“图片缺失”，请先安装原图，再重启 ComfyUI。

节点依赖均使用 ComfyUI 已有的 Pillow、NumPy、PyTorch、aiohttp。

高级：`COMFYUI_POSE_GALLERY_LIBRARY` 可指定服务器上已有的完整图库根目录（含 data、img、thumbs）；默认使用本插件 `library/`。浏览器只能读取元数据允许的图片，路径穿越和外部文件符号链接会被拒绝。

## Depth Anything → MOSS SFT 50 步

导入 `example_workflows/pose_gallery_moss_sft50.json`；`.api.json` 是服务端 API 格式。

链路：Pose Gallery → Depth Anything V2 Large → 1056×1408 等比缩放 → MOSS-Image Color/Depth Control → MOSS SFT → 保存。

工作流依赖：

- ComfyUI 0.43.0（本机已测试），含原生 MOSSImageControl、MOSS 模型支持。
- `comfyui_controlnet_aux`，Depth Anything V2 Large 权重。
- `models/diffusion_models/moss/moss_image_sft_bf16.safetensors`
- `models/text_encoders/moss/qwen3.5_9b_int8_convrot.safetensors`
- `models/vae/moss/flux2-vae.safetensors`
- `models/loras/moss/moss_image_color_depth_control.safetensors`，来自 [Comfy-Org/MOSS-Image](https://huggingface.co/Comfy-Org/MOSS-Image)，适配器作者 [darask0](https://huggingface.co/darask0/MOSS-Image-color-depth-control)。

50 步、CFG 3、Euler、sgm_uniform、Shift 5、负向跳过单流层 22。控制 LoRA 强度 1.0；深度强度 0.75，开始 0，结束 0.5。提前结束深度控制用于减少素体外观。深度输入采用近白远黑的灰度图。

切换姿势时，同时调整正向提示词中的动作；描述服装、脸部、环境和光线。深度图约束轮廓与前后关系，手指和脸部仍由模型生成。调整分辨率时，同时修改深度缩放和 Empty Flux 2 Latent 的尺寸。若想更严格约束，逐步调高 depth strength/end_percent。

运行保存路径相对于 **ComfyUI output**：

- `images/moss/pose/depth/pose_depth_*.png`
- `images/moss/pose/result/moss_sft50_pose_*.png`

PNG 包含实际 API 参数和可导入工作流。开发工作区的 `images/moss/pose/` 另外保留实测文件、历史和界面证据；这些本机文件不包含在此源码仓库中。

## 参考简化版 ER-SDE 工作流

导入 `example_workflows/pose_gallery_moss_sft50_reference.json` 使用参考版；对应的 `.api.json` 可通过 ComfyUI API 执行。该版本参考 `moss_image_control_depth_simple.json` 的采样配置，接入 Pose Gallery 和 Depth Anything，并使用常规 SFT 50 步。

- 参考文件的 101 号节点使用 `moss_image_color_depth_control.safetensors`，本机对应 `moss/moss_image_color_depth_control.safetensors`。
- 该 [Comfy-Org 文件](https://huggingface.co/Comfy-Org/MOSS-Image/blob/main/loras/moss_image_color_depth_control.safetensors) 与作者的 [moss-control.safetensors](https://huggingface.co/darask0/MOSS-Image-color-depth-control/blob/main/moss-control.safetensors) 字节一致，SHA-256 均为 `e5c0c3efd05e4269207a39de6005798f14c90c6687c89c54eaffe4b76c43a763`。
- 采用参考参数：ER-SDE、simple、TSR 0.95 / sigma 1、CFG 3、Shift 5、深度强度 0.5、控制范围 0–0.6。
- 参考文件 SLG 标题写着第 22 层，实际 `single_layers` 为 `24`；此版本明确采用实际数值 24。
- 参考文件外层为 24 步，本版保留用户要求的 50 步。主模型使用本机 SFT BF16；Turbo LoRA 不启用。
- 深度图按原比例缩放到约 1 MP，通过 GetImageSize 自动连接潜空间宽高；使用兼容 MOSS 的 EmptyFlux2LatentImage。
- 结果保存为 `images/moss/pose/depth/reference_depth_*.png` 和 `images/moss/pose/result/reference_ersde_sft50_*.png`（相对于 ComfyUI output）。

## 素材和许可

节点代码及改编的画廊页面遵循 MIT；保留上游声明，详见 LICENSE、NOTICE.md。图片及原始数据权利属于原作者ギア，中文数据由 Anhao 整理，不适用代码 MIT 许可。仓库的 `library/thumbs/` 和 `library/data/` 包含来自原图库的缩略图及中文索引，并保留素材来源和上游许可说明；这些素材不适用节点代码的 MIT 许可。原尺寸 PNG 单独安装到 `library/img/`，该目录不纳入 Git。原站链接和来源说明保留，已移除上游统计脚本。

## 验证

`python -m unittest discover -s tests -v` 检查目录边界、非法 ID、文件缺失和符号链接逃逸。本次还实际验证了 ComfyUI 注册、图库接口、浏览器搜索与视角切换、选择写回和完整 SFT 50 步生成。
