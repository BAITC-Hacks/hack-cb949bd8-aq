#!/usr/bin/env python3
"""Classify product images by the proportion of red pixels they contain.

Usage:
    python detect_defect.py
    python detect_defect.py defect.png --threshold 0.02
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def red_ratio(image_path: Path, min_saturation: int = 80, min_value: int = 60) -> float:
    """Return the fraction of image pixels that are visibly red.

    HSV is used because hue separates red from brightness. Red wraps around the
    hue scale in OpenCV, so both ends of the scale must be included.
    """
    # imdecode keeps Windows Unicode paths intact (cv2.imread may not).
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = cv2.inRange(hsv, (0, min_saturation, min_value), (10, 255, 255))
    upper_red = cv2.inRange(hsv, (170, min_saturation, min_value), (180, 255, 255))
    red_mask = cv2.bitwise_or(lower_red, upper_red)
    return float(np.count_nonzero(red_mask)) / red_mask.size


def classify(image_path: Path, threshold: float) -> tuple[str, float]:
    ratio = red_ratio(image_path)
    return ("DEFECT" if ratio >= threshold else "OK"), ratio


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report DEFECT when enough visible red is present in an image."
    )
    parser.add_argument(
        "images",
        nargs="*",
        type=Path,
        default=[Path("ok.png"), Path("defect.png")],
        help="Images to inspect (default: ok.png defect.png)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.01,
        help="Minimum red-pixel share for DEFECT, from 0 to 1 (default: 0.01)",
    )
    args = parser.parse_args()

    if not 0 <= args.threshold <= 1:
        parser.error("--threshold must be between 0 and 1")

    had_error = False
    for image_path in args.images:
        try:
            result, ratio = classify(image_path, args.threshold)
            print(f"{image_path}: {result} (red area: {ratio:.2%})")
        except ValueError as error:
            print(f"ERROR: {error}")
            had_error = True

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
