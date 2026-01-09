"""
Image Resize Script for Patch Website

This script resizes images in the public folder to reduce file sizes
while maintaining quality. Only images over MIN_SIZE_MB that are larger
than MAX_WIDTH will be scaled down.

Usage:
    python resize_images.py              # Dry run (shows what would be resized)
    python resize_images.py --apply      # Actually resize the images

Requirements:
    pip install Pillow
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is not installed. Run: pip install Pillow")
    sys.exit(1)

# Configuration
MAX_WIDTH = 1920  # Maximum width in pixels
QUALITY = 85      # JPEG quality (1-100)
MIN_SIZE_MB = 1.0 # Minimum file size in MB to resize
PUBLIC_DIR = Path(__file__).parent / "public"

# Image extensions to process
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

# Folders/files to skip
SKIP_PATTERNS = {'node_modules', '.git', 'favicon', 'noise.png'}


def should_skip(path: Path) -> bool:
    """Check if this path should be skipped."""
    for pattern in SKIP_PATTERNS:
        if pattern in str(path):
            return True
    return False


def get_image_files(directory: Path) -> list[Path]:
    """Recursively find all image files in directory."""
    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(directory.rglob(f"*{ext}"))
        images.extend(directory.rglob(f"*{ext.upper()}"))
    return [img for img in images if not should_skip(img)]


def get_file_size_mb(path: Path) -> float:
    """Get file size in MB."""
    return path.stat().st_size / (1024 * 1024)


def resize_image(image_path: Path, dry_run: bool = True) -> dict:
    """
    Resize an image if it's larger than MAX_WIDTH.

    Returns a dict with info about what was done.
    """
    result = {
        'path': image_path,
        'original_size_mb': get_file_size_mb(image_path),
        'new_size_mb': None,
        'original_dimensions': None,
        'new_dimensions': None,
        'action': 'skipped',
        'error': None
    }

    try:
        # Skip if file is under minimum size
        if result['original_size_mb'] < MIN_SIZE_MB:
            result['action'] = 'too_small'
            return result

        with Image.open(image_path) as img:
            result['original_dimensions'] = img.size
            width, height = img.size

            # Skip if already smaller than max width
            if width <= MAX_WIDTH:
                result['action'] = 'already_small'
                return result

            # Calculate new dimensions
            ratio = MAX_WIDTH / width
            new_width = MAX_WIDTH
            new_height = int(height * ratio)
            result['new_dimensions'] = (new_width, new_height)

            if dry_run:
                result['action'] = 'would_resize'
                # Estimate new size (rough approximation)
                result['new_size_mb'] = result['original_size_mb'] * (ratio ** 2) * 0.8
                return result

            # Actually resize
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Determine format and save
            format_map = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG', '.webp': 'WEBP'}
            ext = image_path.suffix.lower()
            save_format = format_map.get(ext, 'JPEG')

            # Handle RGBA images for JPEG
            if save_format == 'JPEG' and resized.mode in ('RGBA', 'P'):
                resized = resized.convert('RGB')

            # Save with optimization
            save_kwargs = {'optimize': True}
            if save_format == 'JPEG':
                save_kwargs['quality'] = QUALITY
            elif save_format == 'PNG':
                save_kwargs['compress_level'] = 9
            elif save_format == 'WEBP':
                save_kwargs['quality'] = QUALITY

            resized.save(image_path, save_format, **save_kwargs)
            result['new_size_mb'] = get_file_size_mb(image_path)
            result['action'] = 'resized'

    except Exception as e:
        result['action'] = 'error'
        result['error'] = str(e)

    return result


def format_size(mb: float) -> str:
    """Format size in MB nicely."""
    if mb < 1:
        return f"{mb * 1024:.0f} KB"
    return f"{mb:.2f} MB"


def main():
    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN - No files will be modified")
        print("Run with --apply to actually resize images")
        print("=" * 60)
    else:
        print("=" * 60)
        print("APPLYING CHANGES - Resizing images")
        print("=" * 60)

    print(f"\nScanning: {PUBLIC_DIR}")
    print(f"Min file size: {MIN_SIZE_MB} MB")
    print(f"Max width: {MAX_WIDTH}px")
    print(f"JPEG quality: {QUALITY}")
    print()

    images = get_image_files(PUBLIC_DIR)
    print(f"Found {len(images)} images\n")

    results = {
        'would_resize': [],
        'resized': [],
        'already_small': [],
        'too_small': [],
        'error': [],
        'skipped': []
    }

    total_original = 0
    total_new = 0

    for image_path in sorted(images):
        result = resize_image(image_path, dry_run=dry_run)
        results[result['action']].append(result)

        if result['action'] in ('would_resize', 'resized'):
            total_original += result['original_size_mb']
            if result['new_size_mb']:
                total_new += result['new_size_mb']

            rel_path = image_path.relative_to(PUBLIC_DIR)
            dims = result['original_dimensions']
            new_dims = result['new_dimensions']

            print(f"{'[WOULD RESIZE]' if dry_run else '[RESIZED]'} {rel_path}")
            print(f"  Dimensions: {dims[0]}x{dims[1]} -> {new_dims[0]}x{new_dims[1]}")
            print(f"  Size: {format_size(result['original_size_mb'])}", end="")
            if result['new_size_mb']:
                print(f" -> {format_size(result['new_size_mb'])}")
            else:
                print()

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if dry_run:
        print(f"Images that would be resized: {len(results['would_resize'])}")
    else:
        print(f"Images resized: {len(results['resized'])}")

    print(f"Images under {MIN_SIZE_MB} MB (skipped): {len(results['too_small'])}")
    print(f"Images already under {MAX_WIDTH}px: {len(results['already_small'])}")

    if results['error']:
        print(f"Errors: {len(results['error'])}")
        for r in results['error']:
            print(f"  - {r['path'].relative_to(PUBLIC_DIR)}: {r['error']}")

    if total_original > 0:
        savings = total_original - total_new
        print(f"\nTotal size of large images: {format_size(total_original)}")
        if total_new > 0:
            print(f"After resizing: {format_size(total_new)}")
            print(f"Estimated savings: {format_size(savings)} ({savings/total_original*100:.1f}%)")

    if dry_run and results['would_resize']:
        print(f"\nRun with --apply to resize these {len(results['would_resize'])} images")


if __name__ == "__main__":
    main()
