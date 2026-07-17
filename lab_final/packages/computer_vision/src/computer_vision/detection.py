"""Small NumPy-based colored-region detector used by the ROS adapter."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DetectionResult:
    detected: bool
    color: str
    confidence: float
    area_px: float
    distance_cm: float
    bbox: tuple


def _mask_for_color(image_bgr, color_name):
    blue, green, red = [image_bgr[:, :, index].astype(np.int16) for index in range(3)]
    if color_name == "red":
        return (red > 100) & (red > blue * 1.3) & (red > green * 1.3)
    if color_name == "green":
        return (green > 100) & (green > blue * 1.3) & (green > red * 1.3)
    if color_name == "blue":
        return (blue > 100) & (blue > green * 1.3) & (blue > red * 1.3)
    if color_name == "yellow":
        return (red > 100) & (green > 100) & (blue < 120)
    if color_name == "white":
        return (red > 180) & (green > 180) & (blue > 180)
    raise ValueError(f"Unsupported color: {color_name}")


def detect_colored_line(image_bgr, color_name, thresholds=None):
    """Detect the largest colored region and return a typed result.

    ``thresholds`` is reserved for calibrated deployments; the default detector
    uses robust BGR predicates so this helper remains testable without OpenCV.
    """
    del thresholds
    if image_bgr.ndim != 3 or image_bgr.shape[2] != 3:
        raise ValueError("image_bgr must have shape (height, width, 3)")

    mask = _mask_for_color(image_bgr, color_name)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return DetectionResult(False, "", 0.0, 0.0, 0.0, (0, 0, 0, 0))

    x, y = int(xs.min()), int(ys.min())
    width, height = int(xs.max() - x + 1), int(ys.max() - y + 1)
    area = float(len(xs))
    image_area = float(mask.shape[0] * mask.shape[1])
    bottom_fraction = (mask.shape[0] - (y + height)) / max(mask.shape[0], 1)
    return DetectionResult(
        True,
        color_name,
        min(1.0, area / image_area),
        area,
        max(0.0, bottom_fraction * 100.0),
        (x, y, width, height),
    )
