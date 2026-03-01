# pic2art

Transform photos into LEGO mosaic style

将照片转换为 LEGO 马赛克风格

## Features

Converts photos into realistic LEGO brick effects with physical details: brick gaps, plastic reflections, color variations, and ambient occlusion.

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

## Inspiration

Inspired by the LEGO mosaic artwork of [Geoffroy Amelot](https://supergeoffroy.tumblr.com/archive/2013/10).

Notable works:
- [Mona Lisa](https://supergeoffroy.tumblr.com/image/62165078257)
- [Van Gogh](https://supergeoffroy.tumblr.com/image/62319521313)

## License

MIT
