# 机器与物品通用提示词

修订：2026-11-13。适用于单件库存机器、容器、工具、材料与布偶；人物不在本仓库范围。本页是本目录唯一的完整提示词，AGENTS 与总方案只维护执行入口。GitHub 建议、采用理由、未采用内容与生图测试见 [PROMPT-RESEARCH.md](RESEARCH.md)。

## 使用方式

1. 先查看同用途原版 PNG。通常选一个结构／风格主参考，确有额外材质需要时再加参考；每张注明用途，通过工具真实图片输入传入。仅在提示词里写文件路径不等于传入图片。[G1][G2]
2. 极小参考可先按整数最近邻放大再传入，完整保留画布、留白和Alpha，并注明原生尺寸。这是输入参考的逐像素复制；不是生图结果缩小。记录倍率与哈希，验证每个原像素变为相同颜色的方块。本轮48×48炉子用16倍、16×32药瓶用32倍有改善，倍率不是通用常数。[G1]
3. 填下面的主体、设计范围、目标尺寸、视角、关键结构、材质与留白。参考里能直接看出的风格用简短文字确认；不用一串时代或画质标签代替参考。[G1]
4. 把通用提示词中的占位符全部替换；“设计范围”和“类别描述”分别只选一个分支。提示词不包含验收流程、来源编号或任务记录。
5. 默认真正透明背景，并启用工具透明输出；不透明单色背景仅用于明确指定的实验，不再默认绿幕。透明与单色背景要求互斥。
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

Background: actual transparent PNG, with transparent exterior and open gaps. Keep the sprite opaque with hard alpha edges; no checkerboard pattern or colored matte. Keep the complete object inside the specified framing. One object only; no ground, cast shadow, captions, borders or visible grid.
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

### 不透明单色实验分支

仅在实验明确要求时，将整个 Background 句替换为：

```text
Background: one opaque flat color [EXACT RGB], including open gaps. No gradients or cast shadows. Keep the complete object inside the specified framing.
```

指定 RGB 仍须实测；本次纯色试验未能精确保持指定颜色。

若有真实半透明材质需求，另定 Alpha 与游戏混合要求，不同时要求所有主体像素不透明。

### 工具适配

- 当前通用生图工具：使用上述完整骨架。颜色在提示词中按材质用途描述，精确 RGB 留在规格和验收记录里；不靠长十六进制列表或固定色数保证风格。[G1][G2]
- 若用户另选 Retro Diffusion：其官方 MCP 建议主要描述主体，由所选 style 控制像素风；使用实际宽高、style、参考图参数，并查所选 style 的限制。不要把“不要写 pixel art”泛化给所有模型，也不要凭提示词假装已切换专用模型。[G3]
- GitHub 中的缩小、网格恢复、量化和抠色建议属于后处理，必须另存并标注处理阶段；完整制作任务可按下方原生整理流程执行，用户明确只要模型直出时不追加处理。[G2][G4]

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


## 完整制作任务模板


保存日期：2026-11-13。

依据：CorpPresence 提交 `1b6d4c780ce25e0f34d36edfdeed3580213d830c` 已验证的流程、工具与矿化机样例。此模板用于交给能操作生图工具、文件和Aseprite的助手执行完整任务；不是单独粘贴进图像模型的提示词。不包含后续立式矿化机的造型方案或追加要求。

将下面方括号替换为实际内容，即可整段使用。

## 可直接复制的任务提示词

```text
请按“生成造型 → 确定性转换 → 原生像素整理 → 验收交付”的流程，为我制作一张游戏像素精灵。

【任务参数】
主体与用途：[物品/机器名称及功能]
设计方式：[全新设计 / 忠实重绘 / 保留造型局部修改，选择一种]
目标实际PNG尺寸：[宽]×[高]像素
目标游戏与风格：[游戏名称或具体风格参考]
结构主参考：[资源/图片及要借鉴的结构；可从项目资料查找]
材质参考：[资源/图片及要借鉴的金属、玻璃、涂装等]
必须保留或排除的内容：[具体内容；没有则写无]
仓库位置：[本地仓库路径或GitHub地址]
输出目录：[本地工作目录]
本次交付范围：独立原尺寸PNG、可编辑源文件、生成原稿、转换参数和像素整理记录；不自动接入游戏或提交GitHub。

【先读取现有规范与工具】
如果使用CorpPresence项目，先读取：
- art/AGENTS.md
- art/NATIVE-WORKFLOW.md
- art/STYLE-REFERENCE.md中相关类别
- art/TASK-TEMPLATE.md
- art/tools/native/README.md
- art/examples/mineral-native/README.md及其manifest和编辑记录
其他项目沿用下面的流程，按项目实际情况替换参考与工具路径。不要把矿化机的48×64、调色板、造型或修改比例作为所有素材的固定规格。

【1. 设计与生成】
先根据目标原生尺寸安排轮廓、部件比例、留白与细节预算，说明结构和材质分别参考什么。全新设计与忠实重绘分开处理：前者不照搬旧造型，后者不随意移动或重设计应保留的部件。

使用图像生成工具制作独立主体，默认真正透明背景及内部空隙，主体不透明，不使用默认绿幕。要求统一逻辑像素网格、有限的实测色板、单色平涂区域和硬边分面。以有目的的短高光、邻接暗面、接缝和端部表现材质，避免渐变、纹理噪点、抖动、抗锯齿、光晕和整圈白色描边。无场景、文字说明或对照板。

保存生成原文件、实际提示词、工具参数与SHA256。读取真实宽高、RGB和Alpha，不把提示中的尺寸或“透明输出”开关当成验收结果。模型未做到目标尺寸或精确颜色时如实记录，不反复追加同义提示后宣称成功。

【2. 确定性转换】
本任务允许转换后原生整理。保持生成原稿不变，转换输出另存为草稿。
先判断是否存在可信的统一像素网格；没有证据时明确称为有损转换，不称无损恢复。记录目标尺寸、取样方法、色板来源、颜色距离、Alpha阈值、裁切、原点及其他实际参数。

优先使用项目已有工具，少量比较中心采样与中心区域众数等方法，按细线、连接、分面和关键识别点的保留情况选择。不要默认弹性切格更好，也不要无限调参。色板按素材材质选择，原版与MOD来源分别标注；不机械套用样例色板。量化和透明阈值的适用性要检查。

转换稿只满足部分文件规格，不能直接作为美术验收通过的依据。源图已经缺失或画错的结构，采样不能自动补回。

【3. 原生像素整理】
在最终[宽]×[高]网格上完成整理。Aseprite集成可用时优先使用，保留可编辑源稿，分别保存自动转换层、结构整理层与材质细化层。

先检查轮廓、部件用途、连接、遮挡、支承、线宽及重复图案，再整理连续平面和材质。用明确的像素段及二维色块处理反光，不给所有边缘加白线，不把量化杂点当作金属纹理。保留有实际用途的单像素细节，不能只为降低色数而删结构。已确认造型优先局部编辑，不反复全图重生成。

记录每轮修改像素的坐标、前后RGBA和用途；分别报告每轮修改数与最终相对自动稿的净变化数，去除重叠，不能直接相加。不要把人工设计的像素修改清单描述成自动修复算法。

【4. 验证】
在实际文件上核对：
- PNG真实宽高符合目标，色板来源明确；新作硬边精灵通常只有Alpha=0/255。
- 在1×下能辨认主要轮廓和功能部件；连接、支撑、孔洞、格栅及连续平面合理。
- 必要时另存最近邻整数倍检查图或同倍率对照；检查预览不能替代原尺寸交付。
- 锁定区域与透明轮廓没有意外改变；有意修改的范围明确记录。
- 修改记录与PNG逐像素一致；源稿重新导出与最终PNG的RGBA一致。
- 记录实际颜色数、Alpha分布、主体包围盒、哈希及每轮/净修改像素数。

使用项目已有重放测试验证确定性步骤。连通组件为1只能证明像素相连，网格或色板满分不能证明机械合理性或美术质量。样例重放通过也不证明新素材已经通过视觉或游戏验证。

【5. 交付与结论】
交付独立原尺寸PNG、可编辑源文件、生成原稿、转换参数、像素修改清单和简短验收说明。展示最终精灵，提供可点击的文件链接。

明确区分：
1. 模型原始输出；
2. 自动转换草稿；
3. 原生像素整理后的成品；
4. 游戏接入与实测状态。

只有模型返回的未处理原文件本身满足全部要求，才称“模型直出可用”。经过重采样、限色、Alpha处理或像素修改的结果，称为转换/原生整理结果，不隐藏编辑贡献。

本次无需启动或部署游戏。未做的引擎过滤、PPU、pivot、图集、玩法占格及实际显示检查如实标明；不把像素文件合格等同游戏验证通过。
```

## 只测试模型直出时的替换句

将任务首句和交付范围改为下面这段，并删除“确定性转换”和“原生像素整理”两节：

```text
本次只测试模型直出能力。使用图像生成工具后，保留原始返回文件并实测宽高、RGB、Alpha、网格和结构。不要缩放、限色、阈值化、抠图或逐像素修改后再交作直出结果。未达标时直接报告实际偏差，交付原文件、提示和测量记录。
```

## 依据入口

- [已验证工作流](https://github.com/aamobe/CorpPresence/blob/1b6d4c780ce25e0f34d36edfdeed3580213d830c/art/NATIVE-WORKFLOW.md)
- [工具说明](https://github.com/aamobe/CorpPresence/blob/1b6d4c780ce25e0f34d36edfdeed3580213d830c/art/tools/native/README.md)
- [矿化机完整样例](https://github.com/aamobe/CorpPresence/tree/1b6d4c780ce25e0f34d36edfdeed3580213d830c/art/examples/mineral-native)
