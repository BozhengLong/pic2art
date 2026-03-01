# pic2art

Transform photos into LEGO mosaic style

## Features

Convert photos into realistic LEGO brick effects with physical details: brick gaps, plastic reflections, color variations, and ambient occlusion.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python lego_mosaic.py
```

The program automatically recommends 5 preset options for rendering.

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
| `--colors` | 22 | Palette colors |
| `--gap` | 0.6 | Brick gap strength (0~1.0) |
| `--fresnel` | 0.5 | Plastic reflection (0~1.0) |
| `--color-var` | 0.4 | Color variation (0~1.0) |
| `--ao` | 0.5 | Ambient occlusion (0~1.0) |

## Requirements

- Python 3.7+
- Pillow >= 9.0.0
- NumPy >= 1.21.0

## License

MIT

