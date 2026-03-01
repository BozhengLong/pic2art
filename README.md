# pic2art

Transform photos into artistic styles with pure code

将照片转换为艺术风格的纯代码工具

---

## Gallery

**LEGO Mosaic Style** - Inspired by [Geoffroy Amelot](https://supergeoffroy.tumblr.com/archive/2013/10)

<table>
  <tr>
    <td align="center">
      <a href="https://supergeoffroy.tumblr.com/image/62165078257">
        <img src="https://64.media.tumblr.com/8e0a8c8f0e0e0e0e0e0e0e0e0e0e0e0e/tumblr_mu3q3qQ3Q31qzun8oo1_1280.jpg" width="300" alt="Mona Lisa LEGO Mosaic"/>
        <br/>Mona Lisa
      </a>
    </td>
    <td align="center">
      <a href="https://supergeoffroy.tumblr.com/image/62319521313">
        <img src="https://64.media.tumblr.com/tumblr_mu6q6qQ3Q31qzun8oo1_1280.jpg" width="300" alt="Van Gogh LEGO Mosaic"/>
        <br/>Van Gogh
      </a>
    </td>
  </tr>
</table>

---

## About

A pure-code image stylization tool. Currently supports **LEGO Mosaic** style with realistic physical details: brick gaps, plastic reflections, color variations, and ambient occlusion.

纯代码实现的图片风格化工具。当前支持 **LEGO 马赛克**风格，模拟砖缝、塑料反光、颜色微差、环境光遮蔽等物理细节。

### Styles

- ✅ **LEGO Mosaic** - Available now
- 🔲 **Pixel Art** - Planned
- 🔲 **Cross-stitch** - Planned

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python lego_mosaic.py
```

The program will recommend 5 preset options and render after selection.

### CLI Mode

```bash
python lego_mosaic.py --in photo.png --out result.png
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--grid-w` | 16 | Horizontal stud count |
| `--grid-h` | 24 | Vertical stud count |
| `--tile` | 64 | Pixels per stud |
| `--colors` | 22 | Palette colors after quantization |
| `--gap` | 0.6 | Brick gap strength (0~1.0) |
| `--fresnel` | 0.5 | Plastic reflection strength (0~1.0) |
| `--color-var` | 0.4 | Color variation strength (0~1.0) |
| `--ao` | 0.5 | Ambient occlusion strength (0~1.0) |

## Requirements

- Python 3.7+
- Pillow >= 9.0.0
- NumPy >= 1.21.0

## License

MIT
