# pic2art

将照片转换为 LEGO 马赛克风格

## 功能

将照片转换为逼真的乐高积木效果，模拟砖缝、塑料反光、颜色微差、环境光遮蔽等物理细节。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 交互模式

```bash
python lego_mosaic.py
```

程序会自动推荐 5 档方案，选择后即可渲染。

### 命令行模式

```bash
python lego_mosaic.py --in photo.png --out result.png
```

## 主要参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--grid-w` | 16 | 水平方向积木钉数量 |
| `--grid-h` | 24 | 垂直方向积木钉数量 |
| `--tile` | 64 | 每颗积木钉的像素大小 |
| `--colors` | 22 | 量化后的色板颜色数 |
| `--gap` | 0.6 | 砖缝强度 (0~1.0) |
| `--fresnel` | 0.5 | 塑料反光强度 (0~1.0) |
| `--color-var` | 0.4 | 颜色微差强度 (0~1.0) |
| `--ao` | 0.5 | 环境光遮蔽强度 (0~1.0) |

## 系统要求

- Python 3.7+
- Pillow >= 9.0.0
- NumPy >= 1.21.0

## License

MIT
