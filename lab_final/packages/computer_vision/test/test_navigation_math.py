import math

from computer_vision.control import compute_controller_output
from computer_vision.odometry import integrate_diff_drive


def test_integrate_diff_drive_moves_straight_forward():
    x, y, theta = integrate_diff_drive(0.0, 0.0, 0.0, 0.5, 0.5, 2.0, 0.1)

    assert math.isclose(x, 1.0, abs_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(theta, 0.0, abs_tol=1e-9)


def test_integrate_diff_drive_updates_curved_pose_once():
    x, y, theta = integrate_diff_drive(0.0, 0.0, 0.0, 0.1, 0.2, 1.0, 0.1)

    expected_theta = 1.0
    expected_radius = 0.15
    assert math.isclose(theta, expected_theta, abs_tol=1e-9)
    assert math.isclose(x, expected_radius * math.sin(expected_theta), abs_tol=1e-9)
    assert math.isclose(y, expected_radius * (1 - math.cos(expected_theta)), abs_tol=1e-9)


def test_integrate_diff_drive_supports_reverse_motion():
    x, y, theta = integrate_diff_drive(0.0, 0.0, 0.0, -0.5, -0.5, 2.0, 0.1)

    assert math.isclose(x, -1.0, abs_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(theta, 0.0, abs_tol=1e-9)


def test_controller_returns_zero_without_detection():
    result = compute_controller_output(None, 0.0, 0.0, 0.1, 0.035, 0.01, 0.001)

    assert result.output == 0.0
    assert result.integral == 0.0


def test_controller_output_is_bounded():
    result = compute_controller_output(1000.0, 0.0, 0.0, 0.1, 0.035, 0.01, 0.001, max_output=2.0)

    assert abs(result.output) <= 2.0
