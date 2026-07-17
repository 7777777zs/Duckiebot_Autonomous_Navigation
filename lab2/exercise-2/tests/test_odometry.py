import math

from odometry.odometry_math import integrate_diff_drive, signed_speed


def test_curved_odometry_updates_heading_once():
    x, y, theta = integrate_diff_drive(0.0, 0.0, 0.0, 0.1, 0.2, 1.0, 0.1)

    assert math.isclose(theta, 1.0, abs_tol=1e-9)
    assert math.isclose(x, 0.15 * math.sin(1.0), abs_tol=1e-9)
    assert math.isclose(y, 0.15 * (1 - math.cos(1.0)), abs_tol=1e-9)


def test_reverse_distance_produces_negative_wheel_speed():
    assert signed_speed(-1.25, 0.5) == -0.5
    assert signed_speed(1.25, 0.5) == 0.5
