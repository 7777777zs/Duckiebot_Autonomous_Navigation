import numpy as np

from computer_vision.detection import detect_colored_line


def solid_bgr(color):
    image = np.zeros((120, 160, 3), dtype=np.uint8)
    image[30:101, 50:111] = color
    return image


def test_detects_red_line():
    result = detect_colored_line(solid_bgr((0, 0, 255)), "red")

    assert result.detected is True
    assert result.color == "red"
    assert result.area_px > 1000
    assert result.bbox[0] == 50


def test_detects_blue_green_yellow_and_white_lines():
    colors = {
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "yellow": (0, 255, 255),
        "white": (255, 255, 255),
    }

    for name, bgr in colors.items():
        result = detect_colored_line(solid_bgr(bgr), name)
        assert result.detected is True, name
        assert result.color == name


def test_no_line_returns_explicit_no_detection():
    result = detect_colored_line(np.zeros((120, 160, 3), dtype=np.uint8), "red")

    assert result.detected is False
    assert result.color == ""
    assert result.area_px == 0.0
    assert result.bbox == (0, 0, 0, 0)
