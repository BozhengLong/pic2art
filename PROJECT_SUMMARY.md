# pic2art 项目开发总结

## 项目概述

**项目名称：** pic2art
**项目定位：** 纯代码实现的图片风格化工具，将照片转换为各种艺术风格
**当前实现：** LEGO 马赛克风格渲染器
**技术栈：** Python 3.7+, NumPy, Pillow
**平台支持：** macOS / Windows / Linux

---

## 开发历程

### 1. 初始需求
- 用户提供了一个基础的 LEGO 马赛克渲染脚本
- 需要改进用户体验，从纯 CLI 参数模式升级为交互式界面

### 2. 交互式 CLI 设计

#### 核心改进
- **无参数运行**：直接 `python lego_mosaic.py` 进入交互模式
- **Tab 补全**：使用 `readline` 模块实现文件路径自动补全（macOS/Linux）
- **自动参数计算**：根据输入图片尺寸智能推荐 5 档方案
  - 迷你 (Mini)
  - 精简 (Light)
  - 标准 (Normal) - 默认推荐
  - 精细 (Fine)
  - 超清 (Ultra)
- **自动输出文件名**：格式 `原文件名_lego_24x36.png`，重名自动加序号
- **循环渲染模式**：渲染完成后可以直接尝试其他方案，无需重启
- **自动打开图片**：渲染完成后可选择用系统默认查看器打开

#### 参数推荐逻辑
```python
# 根据图片短边尺寸分档
if short <= 600:
    bases = [8, 16, 24, 32, 48]
elif short <= 1200:
    bases = [16, 24, 32, 48, 64]
else:
    bases = [24, 32, 48, 64, 96]

# tile 大小根据输出分辨率反推，保持在合理范围
tile = max(32, min(64, round(1600 / long_studs)))
```

### 3. 真实感增强

用户提出需要更真实的 LEGO 渲染效果。分析真实乐高照片的特征后，添加了 4 个物理模拟参数：

#### 3.1 砖缝 (Gap) - 默认 0.6
- **效果**：砖块之间的凹槽缝隙
- **实现**：底部/右侧暗线 + 顶部/左侧高光边
- **系数**：`gap * 0.35 * gap_mask`

#### 3.2 塑料反光 (Fresnel) - 默认 0.5
- **效果**：积木钉边缘的塑料反光，模拟 Fresnel 效应
- **实现**：钉子边缘区域 (d > 0.65) 增加亮度
- **系数**：`fresnel * 0.30 * fresnel_intensity^2`

#### 3.3 颜色微差 (Color Variation) - 默认 0.4
- **效果**：每颗钉随机色偏，模拟不同批次的微小色差
- **实现**：每颗钉添加高斯随机偏移
- **系数**：`std = color_var * 8.0`

#### 3.4 环境光遮蔽 (AO) - 默认 0.5
- **效果**：积木钉根部的环境光遮蔽，接触处更暗
- **实现**：钉子根部环形区域降低亮度
- **系数**：`ao * 0.20` (base) / `ao * 0.15` (stud)

**调优过程**：
- 初版系数过小（0.08-0.15），效果几乎看不出来
- 用户反馈后将系数提升 2.5-3 倍，达到明显可见的效果

### 4. 国际化 (i18n)

#### 语言选择策略
最初考虑过自动检测系统语言，但存在问题：
- 很多中文用户使用英文系统
- 自动检测不可靠

**最终方案**：
- 首次运行时询问语言偏好（中文/English）
- 选择保存到 `.lego_mosaic.conf` 配置文件
- 后续运行自动读取，不再询问
- 支持 `--lang cn/en` 临时切换
- 支持 `--lang cn --save` 永久修改

#### 实现细节
```python
# 优先级：CLI 参数 > 配置文件 > 首次询问
def _init_lang(cli_lang: Optional[str] = None, save: bool = False):
    if cli_lang and cli_lang in STRINGS:
        lang = cli_lang
        if save:
            _save_lang(lang)
    else:
        lang = _load_lang()
        if lang not in STRINGS:
            lang = _ask_lang()
    T = STRINGS[lang]
```

### 5. 项目命名演变

#### 命名讨论过程
1. **初始想法**：`lego-mosaic` - 太窄，只覆盖 LEGO 风格
2. **通用方向**：`mosaic-studio`, `pixel-mosaic` - 仍局限于马赛克类
3. **创意命名**：`pixforge`, `recast`, `prismify`, `artcast` - 过于抽象
4. **回归直白**：`pic-style`, `photo-art` - 通俗易懂
5. **最终选择**：`pic2art` - 简洁明了，遵循 `image2art` 命名惯例

**选择理由**：
- 7 个字符，短小精悍
- 含义清晰：picture to art
- 遵循业界常见命名模式（如 `text2speech`, `img2img`）
- GitHub 上基本无重名
- 适合未来扩展多种风格

### 6. 未来扩展规划

#### 可实现的风格类型

**物理材质模拟**
- ✅ 乐高积木（已实现）
- 十字绣 - X 形针脚 + 布纹底
- 钻石画 - 菱形切面 + 折射闪光
- 拼豆 - 圆形珠子 + 拼板孔洞
- 罗马马赛克 - 不规则石块 + 灰缝
- 彩色玻璃 - Voronoi 多边形 + 铅条

**数字/图形风格**
- 像素画 - 纯色块，最经典
- ASCII 艺术 - 字符映射亮度
- 半色调 - 大小不一的圆点，报纸印刷感
- 点彩派 - 纯色小点密铺
- Low-poly - 三角剖分，低多边形
- 六边形网格 - 蜂巢结构

**绘画模拟**
- 油画 - 笔触方向跟随边缘
- 水彩 - 湿边扩散 + 颜色渗透
- 铅笔素描 - 边缘检测 + 交叉排线
- 木刻版画 - 高对比 + 木纹

#### 代码能力上限
- ✅ 能做：所有基于规则、数学、几何的 2D 视觉效果
- ❌ 做不到：需要"理解内容"的 AI 风格迁移、真正的 3D 渲染、照片级真实材质

---

## 技术实现细节

### 核心渲染流程

```python
def lego_mosaic(src_img: Image.Image, p: Params) -> Image.Image:
    # 1. 按目标宽高比裁剪
    cropped = center_crop_to_aspect(src_img, p.grid_w / p.grid_h)

    # 2. 下采样到 stud 网格
    down = cropped.resize((p.grid_w, p.grid_h), resample=Image.Resampling.BOX)

    # 3. 颜色量化（中位切割法，无抖动）
    down_q = quantize_palette(down, p.colors)

    # 4. 构建 stud 光照遮罩（一次性预计算）
    inside, base_mult, stud_mult = build_stud_masks(p.tile, p.gap, p.fresnel, p.ao)

    # 5. 逐格渲染
    for gy in range(p.grid_h):
        for gx in range(p.grid_w):
            color = grid[gy, gx].copy()
            # 添加颜色微差
            if p.color_var > 0:
                shift = rng.normal(0, p.color_var * 8.0, size=3)
                color = color + shift
            # 应用光照遮罩
            tile_rgb = color * base_mult
            tile_rgb = np.where(inside > 0.5, color * stud_mult, tile_rgb)
            out[y0:y0+tile, x0:x0+tile, :] = tile_rgb

    # 6. 后处理
    out = apply_vignette(out, p.vignette)
    out = add_noise(out, p.noise, p.seed)

    return Image.fromarray(out.astype(np.uint8))
```

### 光照模拟原理

#### 半球法线计算
```python
# 归一化距离
d = dist / r
# 半球法线向量
nx = (x - cx) / r
ny = (y - cy) / r
nz = sqrt(1 - d^2)  # 半球高度

# 光照方向（左上方）
L = [-0.65, -0.55, 0.52]
intensity = nx*L[0] + ny*L[1] + nz*L[2]
```

#### 高光计算
```python
# 高光位置（左上偏移）
hx = cx - r * 0.35
hy = cy - r * 0.35
# 高斯分布高光
spec = exp(-((x-hx)^2 + (y-hy)^2) / (2 * (r*0.18)^2))
```

### 跨平台兼容性

#### Tab 补全
- **macOS/Linux**：使用 `readline` 模块
- **Windows**：`readline` 不可用，跳过补全功能，手动输入路径

#### 打开文件
```python
if platform.system() == "Darwin":
    subprocess.Popen(["open", path])
elif platform.system() == "Windows":
    os.startfile(path)
else:
    subprocess.Popen(["xdg-open", path])
```

#### 类型注解
- 使用 `Optional[str]` 而非 `str | None`，兼容 Python 3.7+

---

## 使用指南

### 安装依赖
```bash
pip install pillow numpy
```

### 交互模式
```bash
python lego_mosaic.py

# 首次运行会询问语言
Language / 语言:
[1] 中文
[2] English
选择 / Choose [1/2]: 1

# 输入图片路径（支持 Tab 补全）
请输入图片路径 (Tab 补全): ./photo.png

# 选择方案
推荐方案:
  [1] 迷你  8x12   tile=64  -> 输出  512x768
  [2] 精简  16x24  tile=48  -> 输出  768x1152
  [3] 标准  24x36  tile=40  -> 输出  960x1440  (推荐)
  [4] 精细  32x48  tile=32  -> 输出 1024x1536
  [5] 超清  48x72  tile=32  -> 输出 1536x2304

选择方案 [1-5] 或 [c] 自定义 (默认 3): 3

# 渲染完成
✅ 已保存: photo_lego_24x36.png  (960x1440)

[Enter] 换个方案再试  /  [o] 打开图片  /  [q] 退出:
```

### 经典 CLI 模式
```bash
# 基础用法
python lego_mosaic.py --in photo.png --out result.png

# 自定义参数
python lego_mosaic.py --in photo.png \
  --grid-w 32 --grid-h 48 \
  --tile 40 --colors 22 \
  --gap 0.8 --fresnel 0.6 --color-var 0.5 --ao 0.7

# 切换语言
python lego_mosaic.py --lang en
python lego_mosaic.py --lang cn --save  # 永久保存
```

### 参数说明

| 参数 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| `grid_w` | 4~128 | 16 | 水平方向积木钉数量 |
| `grid_h` | 4~128 | 24 | 垂直方向积木钉数量 |
| `tile` | 16~128 | 64 | 每颗积木钉的像素大小 |
| `colors` | 2~256 | 22 | 量化后的色板颜色数 |
| `vignette` | 0~1.0 | 0.20 | 暗角强度 |
| `noise` | 0~0.05 | 0.006 | 高斯噪声强度 |
| `gap` | 0~1.0 | 0.6 | 砖缝强度 |
| `fresnel` | 0~1.0 | 0.5 | 塑料反光强度 |
| `color_var` | 0~1.0 | 0.4 | 颜色微差强度 |
| `ao` | 0~1.0 | 0.5 | 环境光遮蔽强度 |

---

## 项目文件结构

```
pic2art/
├── lego_mosaic.py          # 主程序（645 行）
├── .lego_mosaic.conf       # 语言配置文件（自动生成）
└── PROJECT_SUMMARY.md      # 本文档
```

---

## 开发心得

### 用户体验设计
1. **减少输入**：自动计算参数，提供预设方案
2. **即时反馈**：渲染完立即可以尝试其他方案
3. **智能默认**：Tab 补全、自动文件名、推荐方案
4. **跨平台**：兼容 Windows/macOS/Linux

### 代码设计原则
1. **纯代码实现**：不依赖 AI/ML，完全基于数学和物理模拟
2. **模块化**：渲染逻辑、交互逻辑、i18n 分离
3. **可扩展**：为未来添加更多风格预留空间
4. **向后兼容**：保留经典 CLI 模式

### 性能优化
1. **预计算遮罩**：`build_stud_masks` 只计算一次
2. **NumPy 向量化**：尽可能避免 Python 循环
3. **合理默认值**：输出分辨率控制在 1200-2400px

---

## 下一步计划

### 短期
- [ ] 添加 README.md
- [ ] 添加 requirements.txt
- [ ] 初始化 git 仓库
- [ ] 添加示例图片
- [ ] 发布到 GitHub

### 中期
- [ ] 实现像素画风格
- [ ] 实现十字绣风格
- [ ] 重构为插件架构（`styles/` 目录）
- [ ] 添加风格选择界面

### 长期
- [ ] 实现所有规划的风格
- [ ] 添加批处理模式
- [ ] 性能优化（多线程渲染）
- [ ] 打包为可执行文件

---

## 致谢

本项目由用户与 Claude (Opus 4.6) 协作开发完成。

**开发时间**：2026-03-01
**对话轮次**：约 50+ 轮
**代码行数**：645 行（主程序）

---

*最后更新：2026-03-01*
