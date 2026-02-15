#!/usr/bin/env python3
"""Convert slide screenshot PNGs into a single PDF presentation.

Usage:
    python slides_to_pdf.py <slides_directory> <output_pdf>

Example:
    python slides_to_pdf.py presentation/ presentation/presentation.pdf

The script finds all slide_*.png files in the given directory,
sorts them by slide number, and combines them into a single PDF
where each slide is one page at 1920x1080 (16:9) aspect ratio.
"""

import sys
import re
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install it with: pip install Pillow")
    sys.exit(1)


def natural_sort_key(path: Path) -> int:
    """Extract slide number from filename like slide_1.png, slide_02.png."""
    match = re.search(r"slide_(\d+)", path.stem)
    return int(match.group(1)) if match else 0


def slides_to_pdf(slides_dir: str, output_path: str) -> None:
    slides_path = Path(slides_dir)
    output = Path(output_path)

    # Find all slide images
    patterns = ["slide_*.png", "slide_*.jpg", "slide_*.jpeg"]
    slide_files = []
    for pattern in patterns:
        slide_files.extend(slides_path.glob(pattern))

    if not slide_files:
        print(f"Error: No slide images found in {slides_path}")
        print("Expected files named like: slide_1.png, slide_2.png, ...")
        sys.exit(1)

    # Sort by slide number
    slide_files.sort(key=natural_sort_key)

    print(f"Found {len(slide_files)} slides:")
    for f in slide_files:
        print(f"  - {f.name}")

    # Convert to RGB (PDF doesn't support RGBA)
    images = []
    for slide_file in slide_files:
        img = Image.open(slide_file)
        if img.mode == "RGBA":
            # Composite onto white background
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            images.append(bg)
        elif img.mode != "RGB":
            images.append(img.convert("RGB"))
        else:
            images.append(img)

    # Save as PDF — first image is the base, rest are appended
    output.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        output,
        "PDF",
        resolution=150.0,
        save_all=True,
        append_images=images[1:],
    )

    print(f"\nPDF saved to: {output.absolute()}")
    print(f"Total slides: {len(images)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    slides_to_pdf(sys.argv[1], sys.argv[2])
