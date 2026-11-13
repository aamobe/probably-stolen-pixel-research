> 历史实验/复现，仅按需使用。日常制作改按 [原生分区规范](ART-STANDARD.md)；旧生图和转换步骤不是默认流程。

# 复现已有处理
生成器没有暴露模型版本和seed，不能精确复现生成过程；完整提示词和原始PNG已保存。

记录环境：Python 3.12.14。安装根目录 requirements.txt 中固定依赖。上游Pixel Art Fixer Python及MIT许可证保存在实验目录 vendor/，固定提交见manifest.json。

将本地原版 furnace.png、furnace_on.png、med_bottle_blue.png 放到 inputs/private/，或设置环境变量 PS_ART_REFERENCE_DIR；哈希见第二轮manifest.json。输入目录已被Git忽略，不上传游戏素材库。

从仓库根目录执行以下脚本：
- python experiments/prompt-optimization-20261113/experiment.py
- python experiments/prompt-optimization-20261113/experiment-upscaled.py
- python experiments/prompt-optimization-20261113/register.py
- python experiments/prompt-optimization-20261113/new-machine.py

脚本重写对应results目录的结果与计时统计，不修改输入。包装脚本仅作参考目录适配，上游算法未作功能修改。含原版的对照图重跑后留在本地，被Git忽略。首轮Measure.ps1保留统计方法记录，实际路径以本仓库目录为准。

checksums.json记录初次保存文件的SHA256；重跑计时可能不同。没有执行游戏接入、编译、部署或发布。
