# 本机验证记录

日期：2026-10-28（Asia/Shanghai）。

- ComfyUI 0.43.0，NVIDIA GeForce RTX 5090 D。
- Pose Gallery 已注册；完整图库 1,439 张原图、1,439 张缩略图。
- 浏览器已测试编号搜索、灯箱视角切换、所选图片写回节点和保存工作流后 ID 持久化。
- Depth Anything V2 Large 生成深度图，尺寸 1056×1408。
- MOSS SFT BF16，50 步、CFG 3、Euler、sgm_uniform、Shift 5、负向跳过第 22 层。
- 深度控制 LoRA 强度 1.0、深度强度 0.75，控制范围 0–0.5。
- 完整 API 执行成功，耗时 90.107 秒；深度图和生成图均包含 prompt/workflow PNG 元数据。
- 4 项目录边界与缺失文件单元测试通过；前端 JavaScript 语法检查通过。

图库素材、原图截图、模型权重及本机运行历史不包含在此源码仓库。
