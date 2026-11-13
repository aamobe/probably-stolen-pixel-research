# 机器与物品通用提示词

修订：2026-11-13。适用于单件库存机器、容器、工具、材料与布偶；人物不在本仓库范围。本页是本目录唯一的完整提示词，AGENTS 与总方案只维护执行入口。GitHub 建议、采用理由、未采用内容与生图测试见 [PROMPT-RESEARCH.md](RESEARCH.md)。

## 使用方式

1. 先查看同用途原版 PNG。通常选一个结构／风格主参考，确有额外材质需要时再加参考；每张注明用途，通过工具真实图片输入传入。仅在提示词里写文件路径不等于传入图片。[G1][G2]
2. 极小参考可先按整数最近邻放大再传入，完整保留画布、留白和Alpha，并注明原生尺寸。这是输入参考的逐像素复制；不是生图结果缩小。记录倍率与哈希，验证每个原像素变为相同颜色的方块。本轮48×48炉子用16倍、16×32药瓶用32倍有改善，倍率不是通用常数。[G1]
3. 填下面的主体、设计范围、目标尺寸、视角、关键结构、材质与留白。参考里能直接看出的风格用简短文字确认；不用一串时代或画质标签代替参考。[G1]
4. 把通用提示词中的占位符全部替换；“设计范围”和“类别描述”分别只选一个分支。提示词不包含验收流程、来源编号或任务记录。
5. 默认纯绿背景沿用本工作区约定。要求透明时只用透明分支并启用工具透明输出。绿色主体与绿幕冲突时明确更换背景；绿底文件不属于透明 PNG。
6. 目标尺寸写进提示词；工具有真实尺寸参数时同时设置。没有该参数时如实记录，不把文字要求当成尺寸控制。直接生成文件原样保存；按 [AGENTS.md](../AGENTS.md)验收。用户已授权转换时另走下方分支。

## 通用提示词

以下供当前通用图像生成工具使用。默认中文填写占位符也可以；英文骨架用于保持结构一致，并非声称英文效果更好。

```text
Create one standalone pixel-art inventory sprite of [SUBJECT AND PURPOSE] for Probably Stolen. Target native canvas: [WIDTH]×[HEIGHT] pixels.

Reference: [IMAGE NUMBER, ROLE, ORIGINAL NATIVE SIZE AND WHETHER INTEGER-ENLARGED]. Match the reference's outline weight, shading depth and level of detail.
Design scope: [PRESERVE THE APPROVED DESIGN / CREATE A NEW DESIGN USING ONLY THE REFERENCE'S VISUAL STYLE].
View and framing: [VIEW DIRECTION, VISIBLE TOP/SIDE FACES, OBJECT PROPORTIONS, ANCHOR AND MARGINS].

Structure: [CATEGORY DESCRIPTION AND THE FEW ESSENTIAL VISIBLE PARTS]. Make the silhouette and main functional shapes readable at the target size. Keep connected parts visibly connected and separate parts distinguishable. Simplify secondary details into coherent pixel clusters.

Materials and color: [MAIN MATERIAL COLORS, SHADOW COLORS AND SMALL ACCENT COLORS, WITH THEIR ROLES]. Match the reference's balance of light and dark areas. Keep broad surfaces as continuous flat color clusters. Use discrete shades to explain planes, recesses and overlaps; place short selective highlights where the form needs them. Keep small details subordinate to the main shape.

Use one consistent square pixel scale, crisp stepped contours and deliberate color clusters. No smooth gradients, anti-aliasing, dithering, texture noise, glow or decorative microdetail.

Background: solid pure green #00FF00 everywhere outside the object, including open gaps. Keep the complete object inside the specified framing. One object only; no ground, cast shadow, captions, borders or visible grid.
```

“目标尺寸”“统一像素尺度”是输出要求，仍需读取实际文件验证；这份模板不保证工具遵守。低细节也不等于抹掉原版的必要部件或材质层次。

### 类别描述：只填适用的一项

- **机器**：说明实际功能的输入、处理、输出或控制位置，以及主要连接／支撑关系。没有进出料的机器按真实功能写。可用句式：`[INPUT] connects to [PROCESSING BODY], with [OUTPUT] and [CONTROL] clearly separated.` 先选能说明功能的少数部件，不为凑“机器感”补装饰管路、螺钉和灯。
- **容器、工具、布偶**：写外轮廓和主要身份标记，例如瓶盖—瓶颈—瓶身—标签、手柄—工作端。可用句式：`Recognizable by [SILHOUETTE] and [IDENTITY MARK]; keep [KEY PARTS] distinct.` 按材质保留必要明暗，不照搬机器格栅。
- **矿物、有机原料**：用团块、切面或短色带表达结构，保留参考支持的有组织纹理；不把机壳平面规则变成“所有材料都完全无纹理”。

### 设计范围：互斥分支

- **忠实重绘**：`Preserve the reference's silhouette, proportions, component positions and colors. Simplify only details that cannot read at the target size.`
- **重新设计**：`Create a new silhouette and component arrangement for [FUNCTION]. Use the reference only for rendering style, viewing angle and material treatment.` 不附被排除的旧稿，不同时要求保留旧轮廓。
- **原版改装／状态差分**：输入已批准母版，写 `Change only [REGION AND CHANGE]. Keep the canvas, framing, silhouette and all other regions unchanged.` 生成式编辑不保证锁区；公共区 RGBA 必须另验，不能用相似外观冒充零差异。

### 透明分支

将整个 Background 句替换为：

```text
Background: actual transparent PNG, with transparent exterior and open gaps. Keep the sprite opaque with hard alpha edges; no checkerboard pattern or colored matte.
```

若有真实半透明材质需求，另定 Alpha 与游戏混合要求，不同时要求所有主体像素不透明。

### 工具适配

- 当前通用生图工具：使用上述完整骨架。颜色在提示词中按材质用途描述，精确 RGB 留在规格和验收记录里；不靠长十六进制列表或固定色数保证风格。[G1][G2]
- 若用户另选 Retro Diffusion：其官方 MCP 建议主要描述主体，由所选 style 控制像素风；使用实际宽高、style、参考图参数，并查所选 style 的限制。不要把“不要写 pixel art”泛化给所有模型，也不要凭提示词假装已切换专用模型。[G3]
- GitHub 中的缩小、网格恢复、量化和抠色建议属于后处理，不能自动加入本工作区的直出流程。[G2][G4]

### 已授权转换时的实验分支

1. 独立保存原始生成文件，再生成处理版本，分别记录哈希。使用已知游戏目标尺寸；自动网格检测只供诊断，其猜测不能决定交付尺寸。
2. 比较目标尺寸网格重建与最近邻基线；按同材质参考色组进行颜色映射，抠背景另验。色板不能恢复缺失结构，也不能把所有物品压到同一套九色。
3. 只有留白明显漂移时才测试主体包围盒对齐；它可能改善体量，也可能破坏原本较好的结果。状态差分保持同画布原点，不能逐帧自适应裁剪。
4. 原生尺寸检查轮廓和功能部件，整数放大检查平面与碎点；完整执行 [SCALING.md](VALIDATION.md)。记录算法、版本、参数、Alpha与人工编辑区域。处理图标为“转换实验稿”，不称为原生直出或自动批准。

2026-11-13已运行Pixel Art Fixer Python目标尺寸重建；两张放大参考样本中，最近邻、目标重建、相位重建的最终指标相同，不能把改善全部归功于某个算法。自动检测多次给出错误目标尺寸；详见研究记录。

## 每次生成的最小记录

```text
任务／类别／设计范围：
目标原生尺寸／占格／留白／PPU与pivot（接入时）：
原版参考：文件、资源键、来源版本、SHA256、每张用途：
输入参考副本：整数放大倍率、实际尺寸、SHA256、逐像素复制校验：
主要材质RGB与用途／颜色预算依据：
实际发送的完整提示词：
工具／实际暴露的模型与参数（未暴露写未知）：
生成日期／尝试编号／seed（未暴露写不支持）：
原始输出路径／SHA256／实际宽高／RGB数／Alpha分布：
视觉审核：轮廓、部件关系、视角、明暗面积、细节密度：
技术审核：尺寸、网格、色块、透明度；失败项逐项列出：
差分：母版哈希、允许变化区域、公共区RGBA差异：
用户批准／接入状态：
若已授权处理：原始图与处理图分别记录、算法版本与参数、色板来源、人工修改区域：
```

直出 PNG 本身可以是母版；工具没有输出图层时不虚构可编辑分层源文件。禁止将处理后的文件回填为“原始直出”。

## 小规模验证

先用同一原图、同一主体、同一背景比较旧／新模板；支持 seed 时固定 seed，未暴露时记录随机性。每次只改变正在验证的提示因素；比较整个模板时承认无法归因到某一句。分别报告忠实度、原生可读性、尺寸／网格／Alpha，不能用色数下降证明美感提高。机器样本不能代表所有小物件；单次成功也不能证明稳定性。

2026-11-13首轮炉子A/B未证明新版优于旧版。第二轮两类对象在整数放大参考与授权处理后更忠实；炉子沿用了旧提示词，因此不能归因于新模板。另完成一张48×48新机器转换实验稿，尚未获用户视觉批准或游戏验证。当前模板仍是工作版本；详情见研究记录。
