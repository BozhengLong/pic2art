#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LEGO Stud Mosaic renderer (deterministic, code-based).
Dependencies: Pillow, numpy
Install:
  pip install pillow numpy

Usage:
  python lego_mosaic.py                  # interactive mode
  python lego_mosaic.py --in photo.png   # classic CLI mode
"""

import argparse
import glob
import math
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import readline
except ImportError:
    readline = None

import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
#  i18n
# ---------------------------------------------------------------------------

_CONF_NAME = ".lego_mosaic.conf"

STRINGS = {
    "en": {
        "title": "🧱 LEGO Mosaic Generator",
        "ask_lang": "\n  Language / 语言:\n  [1] 中文\n  [2] English\n  Choose / 选择 [1/2]: ",
        "lang_saved": "  ✅ Saved. English will be used by default (use --lang cn to switch)",
        "ask_path": "\nEnter image path (Tab completion): ",
        "file_not_found": "  File not found: {}",
        "image_info": "\n📷 Image: {} ({}x{})",
        "presets_header": "\nPreset options:",
        "preset_line": "  [{}] {}  {}x{}  tile={}  -> output {}x{}{}",
        "recommended": " (recommended)",
        "presets_footer": "\n  colors: 22  vignette: 0.20  gap: 0.6  fresnel: 0.5  color-var: 0.4  ao: 0.5",
        "choose_preset": "\nChoose [1-5] or [c] custom (default 3): ",
        "invalid_choice": "  Invalid input, using recommended preset",
        "custom_header": "\nCustom parameters (press Enter for defaults):",
        "custom_grid_w": "  Grid width (studs): ",
        "custom_grid_h": "  Grid height (studs): ",
        "custom_tile": "  Tile size (pixels): ",
        "custom_colors": "  Palette colors: ",
        "rendering": "\n⏳ Rendering...",
        "saved": "\n✅ Saved: {}  ({}x{})",
        "next_action": "\n[Enter] Try another  /  [o] Open image  /  [q] Quit: ",
        "opening": "  Opening...",
        "bye": "\n👋 Bye!",
        "preset_names": ["Mini", "Light", "Normal", "Fine", "Ultra"],
    },
    "cn": {
        "title": "🧱 LEGO 马赛克生成器",
        "ask_lang": "\n  Language / 语言:\n  [1] 中文\n  [2] English\n  选择 / Choose [1/2]: ",
        "lang_saved": "  ✅ 已记住，下次自动使用中文 (可用 --lang en 切换)",
        "ask_path": "\n请输入图片路径 (Tab 补全): ",
        "file_not_found": "  文件不存在: {}",
        "image_info": "\n📷 图片: {} ({}x{})",
        "presets_header": "\n推荐方案:",
        "preset_line": "  [{}] {}  {}x{}  tile={}  -> 输出 {}x{}{}",
        "recommended": " (推荐)",
        "presets_footer": "\n  色数: 22  暗角: 0.20  砖缝: 0.6  塑料反光: 0.5  色差: 0.4  AO: 0.5",
        "choose_preset": "\n选择方案 [1-5] 或 [c] 自定义 (默认 3): ",
        "invalid_choice": "  无效输入，使用推荐方案",
        "custom_header": "\n自定义参数 (直接回车使用默认值):",
        "p_grid_w": "网格宽 grid_w (4~128)",
        "p_grid_h": "网格高 grid_h (4~128)",
        "p_tile": "Tile 像素 (16~128)",
        "p_colors": "色数 (2~256)",
        "p_vignette": "暗角强度 (0~1.0)",
        "p_noise": "噪声强度 (0~0.05)",
        "p_gap": "砖缝强度 (0~1.0)",
        "p_fresnel": "塑料反光 (0~1.0)",
        "p_color_var": "颜色微差 (0~1.0)",
        "p_ao": "环境光遮蔽 (0~1.0)",
        "output_res": "\n  -> 输出分辨率: {}x{}",
        "rendering": "\n  渲染参数: {}x{}, tile={}, {}色",
        "saved": "  ✅ 已保存: {}  ({}x{})",
        "after_render": "\n  [Enter] 换个方案再试  /  [o] 打开图片  /  [q] 退出: ",
        "after_open": "\n  [Enter] 换个方案再试  /  [q] 退出: ",
        "preset_labels": ["迷你", "精简", "标准", "精细", "超清"],
    },
    "en": {
        "title": "🧱 LEGO Mosaic Generator",
        "ask_lang": "\n  Language / 语言:\n  [1] 中文\n  [2] English\n  选择 / Choose [1/2]: ",
        "lang_saved": "  ✅ Saved. English will be used next time (use --lang cn to switch)",
        "ask_path": "\nImage path (Tab to complete): ",
        "file_not_found": "  File not found: {}",
        "image_info": "\n📷 Image: {} ({}x{})",
        "presets_header": "\nPresets:",
        "preset_line": "  [{}] {}  {}x{}  tile={}  -> output {}x{}{}",
        "recommended": " (recommended)",
        "presets_footer": "\n  Colors: 22  Vignette: 0.20  Gap: 0.6  Fresnel: 0.5  ColorVar: 0.4  AO: 0.5",
        "choose_preset": "\nChoose [1-5] or [c] custom (default 3): ",
        "invalid_choice": "  Invalid input, using recommended preset",
        "custom_header": "\nCustom parameters (Enter to keep default):",
        "p_grid_w": "Grid width (4~128)",
        "p_grid_h": "Grid height (4~128)",
        "p_tile": "Tile pixels (16~128)",
        "p_colors": "Colors (2~256)",
        "p_vignette": "Vignette (0~1.0)",
        "p_noise": "Noise (0~0.05)",
        "p_gap": "Gap strength (0~1.0)",
        "p_fresnel": "Fresnel (0~1.0)",
        "p_color_var": "Color variation (0~1.0)",
        "p_ao": "Ambient occlusion (0~1.0)",
        "output_res": "\n  -> Output resolution: {}x{}",
        "rendering": "\n  Rendering: {}x{}, tile={}, {} colors",
        "saved": "  ✅ Saved: {}  ({}x{})",
        "after_render": "\n  [Enter] try another  /  [o] open image  /  [q] quit: ",
        "after_open": "\n  [Enter] try another  /  [q] quit: ",
        "preset_labels": ["Mini", "Light", "Normal", "Fine", "Ultra"],
    },
}

# current language strings (set by _init_lang)
T = STRINGS["cn"]


def _conf_path() -> str:
    """Config file path next to the script."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), _CONF_NAME)


def _load_lang() -> Optional[str]:
    """Load saved language preference, or None."""
    path = _conf_path()
    if os.path.isfile(path):
        try:
            with open(path, "r") as f:
                for line in f:
                    if line.startswith("lang="):
                        return line.strip().split("=", 1)[1]
        except Exception:
            pass
    return None


def _save_lang(lang: str):
    """Persist language preference."""
    try:
        with open(_conf_path(), "w") as f:
            f.write(f"lang={lang}\n")
    except Exception:
        pass


def _ask_lang() -> str:
    """First-run language selection."""
    print(STRINGS["en"]["ask_lang"], end="", flush=True)
    choice = input().strip()
    if choice == "1":
        lang = "cn"
    else:
        lang = "en"
    _save_lang(lang)
    print(STRINGS[lang]["lang_saved"])
    return lang


def _init_lang(cli_lang: Optional[str] = None, save: bool = False):
    """Determine language and set global T. Priority: CLI > config > ask."""
    global T
    if cli_lang and cli_lang in STRINGS:
        lang = cli_lang
        if save:
            _save_lang(lang)
    else:
        lang = _load_lang()
        if lang not in STRINGS:
            lang = _ask_lang()
    T = STRINGS[lang]


@dataclass
class Params:
    grid_w: int = 16          # number of studs horizontally
    grid_h: int = 24          # number of studs vertically
    tile: int = 64            # pixels per stud cell
    colors: int = 22          # palette size after quantization
    vignette: float = 0.20    # vignette strength
    noise: float = 0.006      # gaussian noise strength (0.0 to disable)
    seed: int = 42            # noise seed for reproducibility
    gap: float = 0.6          # brick gap/groove strength (0.0 to disable)
    fresnel: float = 0.5      # plastic fresnel rim reflection (0.0 to disable)
    color_var: float = 0.4    # per-stud color micro-variation (0.0 to disable)
    ao: float = 0.5           # ambient occlusion at stud base (0.0 to disable)


def center_crop_to_aspect(img: Image.Image, target_ar: float) -> Image.Image:
    w, h = img.size
    src_ar = w / h

    if src_ar > target_ar:
        new_w = int(h * target_ar)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(w / target_ar)
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)

    return img.crop(box)


def build_stud_masks(tile: int, gap: float = 0.6, fresnel: float = 0.5, ao: float = 0.5):
    """
    Build:
      inside: mask for stud bump area
      base_mult: lighting multiplier for the base plate
      stud_mult: lighting multiplier for the bump surface + specular + rim
    """

    y, x = np.mgrid[0:tile, 0:tile].astype(np.float32)
    cx = (tile - 1) / 2.0
    cy = (tile - 1) / 2.0

    # normalized coords in [-1, 1]
    dx = (x - cx) / (tile / 2.0)
    dy = (y - cy) / (tile / 2.0)

    # base lighting: top-left is brighter
    light = (-dx - dy) / 2.0
    base_mult = 0.93 + 0.06 * light

    # --- gap: brick groove between tiles ---
    if gap > 0:
        gap_th = max(2, int(tile * 0.04))
        gap_mask = np.zeros((tile, tile), dtype=np.float32)
        # bottom and right edges get dark groove
        gap_mask[-gap_th:, :] = 1.0
        gap_mask[:, -gap_th:] = 1.0
        # top and left edges get highlight (light catching the edge)
        hl_th = max(1, gap_th // 2)
        gap_mask[:hl_th, :] = -0.5
        gap_mask[:, :hl_th] = -0.5
        base_mult = base_mult - gap * 0.35 * gap_mask

    # bevel around tile edges
    edge = np.zeros((tile, tile), dtype=np.float32)
    edge_th = max(2, tile // 32)
    edge[:edge_th, :] += 0.035
    edge[:, :edge_th] += 0.035
    edge[-edge_th:, :] -= 0.05
    edge[:, -edge_th:] -= 0.05
    base_mult = np.clip(base_mult + edge, 0.80, 1.12)

    # stud bump geometry
    r = tile * 0.34
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    inside = dist <= r

    # hemisphere normal
    nx = np.zeros_like(dist, dtype=np.float32)
    ny = np.zeros_like(dist, dtype=np.float32)
    nz = np.zeros_like(dist, dtype=np.float32)

    d = dist / (r + 1e-6)
    nx[inside] = (x[inside] - cx) / (r + 1e-6)
    ny[inside] = (y[inside] - cy) / (r + 1e-6)
    nz[inside] = np.sqrt(np.clip(1.0 - d[inside] ** 2, 0.0, 1.0))

    # light direction: top-left, slightly above
    L = np.array([-0.65, -0.55, 0.52], dtype=np.float32)
    L = L / np.linalg.norm(L)

    intensity = nx * L[0] + ny * L[1] + nz * L[2]
    intensity = np.clip(intensity, -1.0, 1.0)

    stud_mult = base_mult.copy()
    stud_mult[inside] = stud_mult[inside] + 0.06 + 0.10 * intensity[inside]

    # specular highlight spot on stud (top-left)
    hx = cx - r * 0.35
    hy = cy - r * 0.35
    spec = np.exp(-(((x - hx) ** 2 + (y - hy) ** 2) / (2 * (r * 0.18) ** 2))).astype(np.float32)
    stud_mult[inside] += 0.08 * spec[inside]

    # --- fresnel: plastic rim reflection on stud edge ---
    if fresnel > 0:
        edge_band = (d > 0.65) & inside
        fresnel_intensity = np.clip((d - 0.65) / 0.35, 0.0, 1.0) ** 2
        stud_mult[edge_band] += fresnel * 0.30 * fresnel_intensity[edge_band]

    # cast shadow around bump to bottom-right
    sx = cx + r * 0.22
    sy = cy + r * 0.22
    shadow = np.exp(-(((x - sx) ** 2 + (y - sy) ** 2) / (2 * (r * 0.35) ** 2))).astype(np.float32)
    ring = (dist > r) & (dist < r * 1.25)
    base_mult[ring] -= 0.06 * shadow[ring]

    # --- ambient occlusion: darken around stud base ---
    if ao > 0:
        ao_ring = (dist > r * 0.75) & (dist < r * 1.25)
        ao_falloff = 1.0 - np.abs(dist - r) / (r * 0.25 + 1e-6)
        ao_falloff = np.clip(ao_falloff, 0.0, 1.0) ** 1.5
        base_mult[ao_ring] -= ao * 0.20 * ao_falloff[ao_ring]
        stud_mult[ao_ring] -= ao * 0.15 * ao_falloff[ao_ring]

    # rim darkening for crisp stud edge
    rim = np.abs(dist - r) <= 0.8
    stud_mult[rim] -= 0.08

    base_mult = np.clip(base_mult, 0.70, 1.15)
    stud_mult = np.clip(stud_mult, 0.70, 1.30)

    return inside.astype(np.float32), base_mult, stud_mult


def quantize_palette(img: Image.Image, colors: int) -> Image.Image:
    """
    Quantize to limited colors, with dithering disabled for a cleaner LEGO look.
    """
    # MEDIANCUT works well for photographs and illustrations
    q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    return q.convert("RGB")


def apply_vignette(out: np.ndarray, strength: float) -> np.ndarray:
    if strength <= 0:
        return out

    h, w, _ = out.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx = (w - 1) / 2.0
    cy = (h - 1) / 2.0
    rr = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)

    vig = 1.0 - strength * np.clip(rr, 0.0, 1.4) ** 1.6
    out = out * vig[..., None]
    return out


def add_noise(out: np.ndarray, noise: float, seed: int) -> np.ndarray:
    if noise <= 0:
        return out
    rng = np.random.default_rng(seed)
    out = out + rng.normal(0, 255 * noise, size=out.shape).astype(np.float32)
    return out


def lego_mosaic(src_img: Image.Image, p: Params) -> Image.Image:
    if p.grid_w <= 0 or p.grid_h <= 0 or p.tile <= 0:
        raise ValueError("grid_w, grid_h, tile must be positive integers")
    if p.colors < 2 or p.colors > 256:
        raise ValueError("colors must be in [2, 256]")

    target_ar = p.grid_w / p.grid_h
    cropped = center_crop_to_aspect(src_img, target_ar)

    # downsample to stud grid
    down = cropped.resize((p.grid_w, p.grid_h), resample=Image.Resampling.BOX)

    # limit palette
    down_q = quantize_palette(down, p.colors)
    grid = np.array(down_q).astype(np.float32)  # (grid_h, grid_w, 3)

    inside, base_mult, stud_mult = build_stud_masks(p.tile, p.gap, p.fresnel, p.ao)

    rng = np.random.default_rng(p.seed)

    out_h, out_w = p.grid_h * p.tile, p.grid_w * p.tile
    out = np.zeros((out_h, out_w, 3), dtype=np.float32)

    # render each stud cell
    for gy in range(p.grid_h):
        for gx in range(p.grid_w):
            color = grid[gy, gx].copy()  # (3,)

            # per-stud color micro-variation
            if p.color_var > 0:
                shift = rng.normal(0, p.color_var * 8.0, size=3).astype(np.float32)
                color = color + shift

            color_tile = color[None, None, :]  # 1x1x3
            tile_rgb = color_tile * base_mult[..., None]
            tile_rgb = np.where(inside[..., None] > 0.5, color_tile * stud_mult[..., None], tile_rgb)

            y0, x0 = gy * p.tile, gx * p.tile
            out[y0:y0 + p.tile, x0:x0 + p.tile, :] = tile_rgb

    # post effects
    out = apply_vignette(out, p.vignette)
    out = add_noise(out, p.noise, p.seed)

    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


# ---------------------------------------------------------------------------
#  Auto parameter calculation
# ---------------------------------------------------------------------------

def _gcd_ratio(w: int, h: int):
    """Return simplified w:h ratio."""
    g = math.gcd(w, h)
    return w // g, h // g


def _snap_grid(dim: int, base: int) -> int:
    """Round dim to nearest multiple of base, minimum base."""
    return max(base, round(dim / base) * base)


def compute_presets(img_w: int, img_h: int):
    """Return 5 preset (label, Params) tuples based on image dimensions."""
    ar = img_w / img_h

    # base stud counts for the short side, 5 tiers
    short = min(img_w, img_h)
    if short <= 600:
        bases = [8, 16, 24, 32, 48]
    elif short <= 1200:
        bases = [16, 24, 32, 48, 64]
    else:
        bases = [24, 32, 48, 64, 96]

    presets = []
    labels = T["preset_labels"]
    for base, label in zip(bases, labels):
        if img_w <= img_h:
            gw = base
            gh = max(base, round(base / ar))
        else:
            gh = base
            gw = max(base, round(base * ar))

        # pick tile so output stays reasonable (target ~1200-2400px on long side)
        long_studs = max(gw, gh)
        tile = max(32, min(64, round(1600 / long_studs)))
        # snap tile to multiple of 8
        tile = max(32, (tile // 8) * 8)

        out_w, out_h = gw * tile, gh * tile
        presets.append((label, Params(grid_w=gw, grid_h=gh, tile=tile), out_w, out_h))

    return presets


# ---------------------------------------------------------------------------
#  Output filename generation
# ---------------------------------------------------------------------------

def auto_output_path(in_path: str, p: Params) -> str:
    """Generate output path like 'photo_lego_24x36.png', auto-increment on conflict."""
    base = os.path.splitext(os.path.basename(in_path))[0]
    directory = os.path.dirname(os.path.abspath(in_path))
    name = f"{base}_lego_{p.grid_w}x{p.grid_h}.png"
    path = os.path.join(directory, name)

    if not os.path.exists(path):
        return path

    i = 2
    while True:
        name = f"{base}_lego_{p.grid_w}x{p.grid_h}_{i}.png"
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            return path
        i += 1


# ---------------------------------------------------------------------------
#  Interactive mode
# ---------------------------------------------------------------------------

def _setup_readline():
    """Enable tab-completion for file paths (skipped on Windows without readline)."""
    if readline is None:
        return
    def completer(text, state):
        expanded = os.path.expanduser(text)
        matches = glob.glob(expanded + "*")
        sep = os.sep
        matches = [m + sep if os.path.isdir(m) else m for m in matches]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    # macOS uses libedit, Linux uses GNU readline
    if readline.__doc__ and "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")


def _ask_image_path() -> str:
    """Prompt user for image path with tab-completion."""
    _setup_readline()
    while True:
        path = input(T["ask_path"]).strip()
        path = os.path.expanduser(path)
        if os.path.isfile(path):
            return path
        print(T["file_not_found"].format(path))


def _show_presets(presets):
    """Display preset options."""
    print(T["presets_header"])
    for i, (label, p, ow, oh) in enumerate(presets, 1):
        rec = T["recommended"] if i == 3 else ""
        print(T["preset_line"].format(i, label, p.grid_w, p.grid_h, p.tile, ow, oh, rec))
    print(T["presets_footer"])


def _choose_params(presets) -> Params:
    """Let user pick a preset or customize."""
    _show_presets(presets)
    print(T["choose_preset"], end="", flush=True)
    choice = input().strip().lower()

    if choice in ("1", "2", "3", "4", "5"):
        return presets[int(choice) - 1][1]
    elif choice == "":
        return presets[2][1]  # default: 标准/Normal
    elif choice == "c":
        return _custom_params(presets[2][1])
    else:
        print(T["invalid_choice"])
        return presets[2][1]


def _custom_params(default: Params) -> Params:
    """Let user tweak individual parameters."""
    def ask_int(prompt, default_val):
        val = input(f"  {prompt} [{default_val}]: ").strip()
        return int(val) if val else default_val

    def ask_float(prompt, default_val):
        val = input(f"  {prompt} [{default_val}]: ").strip()
        return float(val) if val else default_val

    print(T["custom_header"])
    gw = ask_int(T["p_grid_w"], default.grid_w)
    gh = ask_int(T["p_grid_h"], default.grid_h)
    tile = ask_int(T["p_tile"], default.tile)
    colors = ask_int(T["p_colors"], default.colors)
    vignette = ask_float(T["p_vignette"], default.vignette)
    noise = ask_float(T["p_noise"], default.noise)
    gap = ask_float(T["p_gap"], default.gap)
    fresnel = ask_float(T["p_fresnel"], default.fresnel)
    color_var = ask_float(T["p_color_var"], default.color_var)
    ao = ask_float(T["p_ao"], default.ao)
    print(T["output_res"].format(gw * tile, gh * tile))
    return Params(grid_w=gw, grid_h=gh, tile=tile, colors=colors,
                  vignette=vignette, noise=noise, gap=gap, fresnel=fresnel,
                  color_var=color_var, ao=ao)


def _open_file(path: str):
    """Open file with system default viewer (cross-platform)."""
    try:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def interactive_main(cli_lang: Optional[str] = None, save_lang: bool = False):
    """Full interactive workflow."""
    _init_lang(cli_lang, save_lang)
    print(T["title"] + "\n")

    in_path = _ask_image_path()
    img = Image.open(in_path).convert("RGB")
    w, h = img.size
    print(T["image_info"].format(os.path.basename(in_path), w, h))

    presets = compute_presets(w, h)

    while True:
        p = _choose_params(presets)
        out_path = auto_output_path(in_path, p)

        print(T["rendering"].format(p.grid_w, p.grid_h, p.tile, p.colors))
        result = lego_mosaic(img, p)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        result.save(out_path)
        print(T["saved"].format(out_path, result.size[0], result.size[1]))

        print(T["after_render"], end="", flush=True)
        action = input().strip().lower()
        if action == "o":
            _open_file(out_path)
            print(T["after_open"], end="", flush=True)
            action = input().strip().lower()
        if action == "q":
            break


# ---------------------------------------------------------------------------
#  CLI mode (backward compatible)
# ---------------------------------------------------------------------------

def parse_args():
    ap = argparse.ArgumentParser(description="LEGO Mosaic Generator")
    ap.add_argument("--in", dest="in_path", help="input image path (omit for interactive mode)")
    ap.add_argument("--out", dest="out_path", help="output image path")
    ap.add_argument("--lang", choices=["cn", "en"], help="language (cn/en)")
    ap.add_argument("--save", action="store_true", help="save --lang preference for next time")
    ap.add_argument("--grid-w", type=int, default=16)
    ap.add_argument("--grid-h", type=int, default=24)
    ap.add_argument("--tile", type=int, default=64)
    ap.add_argument("--colors", type=int, default=22)
    ap.add_argument("--vignette", type=float, default=0.20)
    ap.add_argument("--noise", type=float, default=0.006)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--gap", type=float, default=0.6)
    ap.add_argument("--fresnel", type=float, default=0.5)
    ap.add_argument("--color-var", type=float, default=0.4)
    ap.add_argument("--ao", type=float, default=0.5)
    return ap.parse_args()


def main():
    args = parse_args()

    # no --in provided → interactive mode
    if not args.in_path:
        interactive_main(cli_lang=args.lang, save_lang=args.save)
        return

    # classic CLI mode
    _init_lang(args.lang, args.save)
    if not os.path.exists(args.in_path):
        raise FileNotFoundError(args.in_path)

    img = Image.open(args.in_path).convert("RGB")
    p = Params(
        grid_w=args.grid_w,
        grid_h=args.grid_h,
        tile=args.tile,
        colors=args.colors,
        vignette=args.vignette,
        noise=args.noise,
        seed=args.seed,
        gap=args.gap,
        fresnel=args.fresnel,
        color_var=args.color_var,
        ao=args.ao,
    )

    out_path = args.out_path or auto_output_path(args.in_path, p)
    out = lego_mosaic(img, p)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    out.save(out_path)
    print(f"Saved: {out_path}  size={out.size}  studs={p.grid_w}x{p.grid_h}  colors={p.colors}")


if __name__ == "__main__":
    main()