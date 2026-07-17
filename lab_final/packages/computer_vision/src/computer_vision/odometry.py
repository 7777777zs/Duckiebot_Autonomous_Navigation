"""Differential-drive pose integration without ROS dependencies."""

import math


def integrate_diff_drive(x, y, theta, v_left, v_right, dt, wheel_base):
    """Integrate one differential-drive timestep using the old pose once."""
    if dt < 0:
        raise ValueError("dt must be non-negative")
    if wheel_base <= 0:
        raise ValueError("wheel_base must be positive")

    velocity = (v_right + v_left) / 2.0
    angular_velocity = (v_right - v_left) / wheel_base

    if abs(angular_velocity) < 1e-9:
        return (
            x + velocity * dt * math.cos(theta),
            y + velocity * dt * math.sin(theta),
            theta,
        )

    new_theta = theta + angular_velocity * dt
    radius = velocity / angular_velocity
    new_x = x + radius * (math.sin(new_theta) - math.sin(theta))
    new_y = y - radius * (math.cos(new_theta) - math.cos(theta))
    return new_x, new_y, new_theta
