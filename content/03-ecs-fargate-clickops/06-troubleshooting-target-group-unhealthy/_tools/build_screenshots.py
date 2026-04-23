#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
RAW_DIR = ROOT / "raw" / "1.target group being unhealthy"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "_diagrams"


CropSpec = tuple[str, str, tuple[int, int, int, int]]


CROPS: list[CropSpec] = [
    (
        "1/image.png",
        "target-group-stale-targets.webp",
        (300, 118, 1875, 1036),
    ),
    (
        "2/image.png",
        "ecs-task-private-ip.webp",
        (1340, 820, 1680, 1025),
    ),
    (
        "3/image.png",
        "target-group-health-check-failed.webp",
        (265, 430, 1885, 1028),
    ),
    (
        "6/image.png",
        "default-security-group-self-reference.webp",
        (20, 120, 1880, 700),
    ),
    (
        "5/image.png",
        "service-config-grace-period-zero.webp",
        (18, 690, 1175, 1090),
    ),
    (
        "9/image.png",
        "ecs-security-group-from-alb.webp",
        (28, 215, 1055, 1015),
    ),
    (
        "10/image.png",
        "service-update-grace-period-90.webp",
        (35, 185, 1045, 1140),
    ),
    (
        "10/image.png",
        "service-update-ecs-security-group.webp",
        (35, 1160, 1045, 1795),
    ),
]


def crop_image(source: Path, destination: Path, box: tuple[int, int, int, int]) -> None:
    with Image.open(source) as image:
        left, top, right, bottom = box
        if left < 0 or top < 0 or right > image.width or bottom > image.height:
            raise ValueError(
                f"Crop {box} is outside image bounds {image.width}x{image.height} for {source}"
            )

        cropped = image.crop(box)
        cropped.save(destination, format="WEBP", quality=88, method=6)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for relative_source, output_name, box in CROPS:
        source = RAW_DIR / relative_source
        destination = OUTPUT_DIR / output_name
        crop_image(source, destination, box)
        print(f"wrote {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
