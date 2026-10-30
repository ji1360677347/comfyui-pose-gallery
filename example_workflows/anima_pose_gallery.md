# Anima Base v1 + Pose Gallery

导入 [`pose_gallery_anima_lllite_v2.json`](pose_gallery_anima_lllite_v2.json)，服务端使用对应 `.api.json`。

## 操作与模型

1. 准备下表权重，更新到包含原生 `ModelPatchLoader` 与 `AnimaLLLiteApply` 的 ComfyUI。
2. 在 Pose Gallery 浏览、筛选姿势，选择视角后点击「使用此姿势 → ComfyUI」。确认节点显示原图。
3. 在正向提示词描述人物、服装、场景和画风；示例提示词不指定固定动作。
4. 点击运行。图库线稿直接作为 LLLite 条件，缩放后尺寸自动传给16通道潜空间。本次为896×1184，无需 Depth Anything。

| 权重 | 相对于 ComfyUI/models 的示例路径 |
| --- | --- |
| Anima Base v1.0 | `diffusion_models/anima/anima-base-v1.0.safetensors` |
| Qwen3 0.6B base | `text_encoders/qwen_3_06b_base.safetensors` |
| Qwen Image VAE | `vae/qwen_image_vae.safetensors` |
| Anima LLLite any-test-like v2 | `model_patches/anima-lllite-any-test-like-v2.safetensors` |

[Anima 模型](https://huggingface.co/circlestone-labs/Anima) · [LLLite 作者与许可](https://huggingface.co/kohya-ss/Anima-LLLite) · [Comfy-Org 权重](https://huggingface.co/Comfy-Org/Anima-LLLite/blob/main/model_patches/anima-lllite-any-test-like-v2.safetensors)。权重不随本仓库分发；请按本机目录重选模型。

30步、CFG4、ER-SDE/simple、种子20261030；控制强度0.75，范围0–0.85，约1MP等比缩放。这是文字加线稿生图，未加入保持同一角色身份的参考图链路。

输出：`output/images/anima/pose_gallery/results/`（人物）和 `poses/`（实际控制图）。

## 实测与边界

2026-10-30，在此前站姿与跪姿测试基础上新增8组。相同提示词、种子、采样参数及控制强度，仅切换姿势ID；8个任务均完成，模型已加载时平均9.4秒/张。主要身体轮廓有跟随，但执行成功不代表成图无瑕疵：

- 单膝跪、俯卧：肩部关节圆圈被转成服装开口或圆形装饰。
- 蹲姿：头部上仰，与参考头部角度存在偏移。
- 服装款式、配饰和脸部可随姿势变化；手指需要人工检查。
- 每组仅测试一个固定种子，未验证多人、所有视角及完整图库的成功率。

![Anima工作流](../docs/images/anima/workflow.png)

![八组姿势对照](../docs/images/anima/comparison.png)

| 姿势原图 | 生成结果 | 目视评价 |
| --- | --- | --- |
| ![站立・双臂上举伸展](../library/img/full_single_P019_side.png) | ![Anima结果](../docs/images/anima/full_single_P019_side_result.png) | `full_single_P019_side` · 9.333秒。侧面朝向、躯干弧度和举臂轮廓跟随。重叠的手臂与手指细节仍需人工检查。 |
| ![站立・单腿后抬](../library/img/full_single_P024_front.png) | ![Anima结果](../docs/images/anima/full_single_P024_front_result.png) | `full_single_P024_front` · 9.334秒。单腿后抬、支撑腿和触头动作跟随；此工作流不保证固定人物身份或服装款式一致。 |
| ![后仰坐・单膝立起](../library/img/full_single_P001_front.png) | ![Anima结果](../docs/images/anima/full_single_P001_front_result.png) | `full_single_P001_front` · 9.369秒。后仰坐、单膝抬起与撑地手位置跟随；裤腿被生成为较短或卷起的款式。 |
| ![侧坐・双腿斜向右侧](../library/img/full_single_P045_diag.png) | ![Anima结果](../docs/images/anima/full_single_P045_diag_result.png) | `full_single_P045_diag` · 9.302秒。斜侧坐、双腿折叠方向和撑地手跟随；新增了参考提示词未要求的肩带与项链。 |
| ![单膝跪・手扶膝](../library/img/full_single_P033_front.png) | ![Anima结果](../docs/images/anima/full_single_P033_front_result.png) | `full_single_P033_front` · 9.365秒。单膝跪、双手扶膝轮廓跟随；肩部关节圆圈被转译为露肩开口，属于控制线残留导致的服装偏差。 |
| ![俯卧・抬腿](../library/img/full_single_P051_front.png) | ![Anima结果](../docs/images/anima/full_single_P051_front_result.png) | `full_single_P051_front` · 9.546秒。俯卧、肘撑与双腿上抬轮廓跟随；肩部关节圆圈被转译为圆形装饰，不宜直接作为无瑕疵成图。 |
| ![蹲姿・手扶膝](../library/img/full_single_P061_side.png) | ![Anima结果](../docs/images/anima/full_single_P061_side_result.png) | `full_single_P061_side` · 9.397秒。侧面蹲姿及手扶膝跟随；头部明显上仰，与参考图头部角度存在偏移。 |
| ![扭身・站姿展臂](../library/img/full_single_P077_front.png) | ![Anima结果](../docs/images/anima/full_single_P077_front_result.png) | `full_single_P077_front` · 9.521秒。扭身、双臂展开与双腿位置总体跟随；手指和躯干转动幅度仍需人工检查。 |

[测试参数与任务ID](pose_gallery_anima_validation.json)。对照图使用真实本地生成结果；图库图片权利说明见仓库 NOTICE.md。
