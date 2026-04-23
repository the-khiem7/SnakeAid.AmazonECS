#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image


CropSpec = tuple[str, str, tuple[int, int, int, int]]


def build_crops(
    *,
    repo_root: Path,
    output_dir: Path,
    crops: list[CropSpec],
    quality: int = 88,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for source_relative, output_name, box in crops:
        source = repo_root / source_relative
        destination = output_dir / output_name
        _crop_image(source=source, destination=destination, box=box, quality=quality)
        print(f"wrote {destination.relative_to(repo_root)}")


def _crop_image(
    *,
    source: Path,
    destination: Path,
    box: tuple[int, int, int, int],
    quality: int,
) -> None:
    with Image.open(source) as image:
        left, top, right, bottom = box
        if left < 0 or top < 0 or right > image.width or bottom > image.height:
            raise ValueError(
                f"Crop {box} is outside bounds {image.width}x{image.height} for {source}"
            )

        cropped = image.crop(box)
        cropped.save(destination, format="WEBP", quality=quality, method=6)
