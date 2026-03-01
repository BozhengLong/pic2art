#!/usr/bin/env python3
"""
pic2art - Transform photos into artistic styles

Unified entry point for all style converters.
"""

import sys
import os
import argparse
from pathlib import Path


STYLES = {
    'lego': {
        'name': 'LEGO Mosaic',
        'module': 'styles.lego_mosaic',
        'description': 'Convert photos to LEGO brick mosaic style'
    },
    # Future styles will be added here
    # 'pixel': {
    #     'name': 'Pixel Art',
    #     'module': 'styles.pixel_art',
    #     'description': 'Convert photos to pixel art style'
    # },
}


def list_styles():
    """Display available styles."""
    print("\n🎨 Available Styles:\n")
    for key, info in STYLES.items():
        status = "✅" if Path(f"styles/{key.replace('_', '')}_mosaic.py" if key == "lego" else f"styles/{key}_art.py").exists() else "🔲"
        print(f"  {status} {key:12} - {info['description']}")
    print()


def run_style(style_key, args):
    """Run the specified style converter."""
    if style_key not in STYLES:
        print(f"❌ Unknown style: {style_key}")
        print(f"   Available styles: {', '.join(STYLES.keys())}")
        sys.exit(1)

    style_info = STYLES[style_key]
    module_path = style_info['module'].replace('.', '/') + '.py'

    if not Path(module_path).exists():
        print(f"❌ Style '{style_key}' is not yet implemented")
        sys.exit(1)

    # Run the style module with remaining arguments
    os.execvp(sys.executable, [sys.executable, module_path] + args)


def interactive_mode():
    """Interactive style selection."""
    print("\n" + "="*50)
    print("  pic2art - Transform Photos into Artistic Styles")
    print("="*50)

    list_styles()

    # Get style choice
    style_keys = list(STYLES.keys())
    print("Select a style:")
    for i, key in enumerate(style_keys, 1):
        print(f"  [{i}] {STYLES[key]['name']}")

    choice = input("\nEnter number [1]: ").strip() or "1"

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(style_keys):
            style_key = style_keys[idx]
        else:
            print("❌ Invalid choice")
            sys.exit(1)
    except ValueError:
        print("❌ Invalid input")
        sys.exit(1)

    # Run the selected style in interactive mode
    run_style(style_key, [])


def main():
    parser = argparse.ArgumentParser(
        description='pic2art - Transform photos into artistic styles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pic2art.py                          # Interactive mode
  pic2art.py --style lego             # Run LEGO style interactively
  pic2art.py --style lego --in photo.png --out result.png
  pic2art.py --list                   # List available styles

For style-specific options, run:
  python styles/lego_mosaic.py --help
        """
    )

    parser.add_argument('--style', '-s', choices=list(STYLES.keys()),
                        help='Style to use')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List available styles')

    # Parse known args, pass the rest to the style module
    args, remaining = parser.parse_known_args()

    if args.list:
        list_styles()
        sys.exit(0)

    if args.style:
        run_style(args.style, remaining)
    else:
        # No style specified, enter interactive mode
        if remaining:
            print("❌ Please specify --style when using other arguments")
            parser.print_help()
            sys.exit(1)
        interactive_mode()


if __name__ == '__main__':
    main()
