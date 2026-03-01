# pic2art

将照片转换为艺术风格的纯代码工具 | Transform photos into artistic styles with pure code

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ 特性 | Features

- 🧱 **LEGO 马赛克风格** - 将照片转换为逼真的乐高积木效果
- 🎨 **物理真实感** - 砖缝、塑料反光、颜色微差、环境光遮蔽
- 🖥️ **交互式 CLI** - 智能推荐方案，Tab 补全，循环渲染
- 🌍 **国际化** - 中文/English 双语支持
- 🔧 **纯代码实现** - 无需 AI/ML，完全基于数学和物理模拟
- 📦 **跨平台** - macOS / Windows / Linux

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
# 克隆仓库
git clone https://github.com/yourusername/pic2art.git
cd pic2art

# 安装依赖
pip install -r requirements.txt
```

### 使用 | Usage

#### 交互模式 | Interactive Mode

```bash
python lego_mosaic.py
```

首次运行会询问语言偏好，然后进入交互式界面：

```
请输入图片路径 (Tab 补全): ./photo.png

推荐方案:
  [1] 迷你  8x12   tile=64  -> 输出  512x768
  [2] 精简  16x24  tile=48  -> 输出  768x1152
  [3] 标准  24x36  tile=40  -> 输出  960x1440  (推荐)
  [4] 精细  32x48  tile=32  -> 输出 1024x1536
  [5] 超清  48x72  tile=32  -> 输出 1536x2304

选择方案 [1-5] 或 [c] 自定义 (默认 3): 3

✅ 已保存: photo_lego_24x36.png  (960x1440)
```

#### 命令行模式 | CLI Mode

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

## 📖 参数说明 | Parameters

| 参数 | 范围 | 默认值 | 说明 | Description |
|------|------|--------|------|-------------|
| `--grid-w` | 4~128 | 16 | 水平方向积木钉数量 | Horizontal stud count |
| `--grid-h` | 4~128 | 24 | 垂直方向积木钉数量 | Vertical stud count |
| `--tile` | 16~128 | 64 | 每颗积木钉的像素大小 | Pixels per stud |
| `--colors` | 2~256 | 22 | 量化后的色板颜色数 | Palette colors |
| `--vignette` | 0~1.0 | 0.20 | 暗角强度 | Vignette strength |
| `--noise` | 0~0.05 | 0.006 | 高斯噪声强度 | Gaussian noise |
| `--gap` | 0~1.0 | 0.6 | 砖缝强度 | Brick gap strength |
| `--fresnel` | 0~1.0 | 0.5 | 塑料反光强度 | Plastic reflection |
| `--color-var` | 0~1.0 | 0.4 | 颜色微差强度 | Color variation |
| `--ao` | 0~1.0 | 0.5 | 环境光遮蔽强度 | Ambient occlusion |

## 🎨 效果展示 | Examples

### 真实感细节 | Realistic Details

LEGO 马赛克渲染器模拟了 4 种物理效果：

1. **砖缝 (Gap)** - 积木块之间的凹槽缝隙
2. **塑料反光 (Fresnel)** - 积木钉边缘的 Fresnel 效应
3. **颜色微差 (Color Variation)** - 不同批次的微小色差
4. **环境光遮蔽 (AO)** - 积木钉根部的阴影

## 🗺️ 未来规划 | Roadmap

### 物理材质模拟 | Physical Materials
- ✅ 乐高积木 (LEGO) - 已实现
- 🔲 十字绣 (Cross-stitch)
- 🔲 钻石画 (Diamond painting)
- 🔲 拼豆 (Perler beads)
- 🔲 罗马马赛克 (Roman mosaic)
- 🔲 彩色玻璃 (Stained glass)

### 数字/图形风格 | Digital Styles
- 🔲 像素画 (Pixel art)
- 🔲 ASCII 艺术 (ASCII art)
- 🔲 半色调 (Halftone)
- 🔲 点彩派 (Pointillism)
- 🔲 Low-poly
- 🔲 六边形网格 (Hexagonal grid)

### 绘画模拟 | Painting Styles
- 🔲 油画 (Oil painting)
- 🔲 水彩 (Watercolor)
- 🔲 铅笔素描 (Pencil sketch)
- 🔲 木刻版画 (Woodcut)

## 🛠️ 技术实现 | Technical Details

- **纯代码实现** - 不依赖 AI/ML，完全基于数学和物理模拟
- **半球法线计算** - 模拟积木钉的 3D 光照效果
- **高斯高光** - 左上方向的塑料反光
- **颜色量化** - 中位切割法，无抖动
- **NumPy 向量化** - 高性能渲染

详细技术文档请参考 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 📋 系统要求 | Requirements

- Python 3.7+
- Pillow >= 9.0.0
- NumPy >= 1.21.0

## 📄 许可证 | License

MIT License

## 🙏 致谢 | Acknowledgments

本项目由用户与 Claude (Opus 4.6) 协作开发完成。

This project was developed in collaboration between user and Claude (Opus 4.6).

---

**开发时间 | Development Date**: 2026-03-01
**代码行数 | Lines of Code**: 645 lines (main program)
