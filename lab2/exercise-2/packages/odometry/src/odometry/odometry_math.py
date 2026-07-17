"""Pure differential-drive math used by the lab2 movement node."""

import math


def integrate_diff_drive(x, y, theta, v_left, v_right, dt, wheel_base):
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
    return (
        x + radius * (math.sin(new_theta) - math.sin(theta)),
        y - radius * (math.cos(new_theta) - math.cos(theta)),
        new_theta,
    )


def signed_speed(distance, speed):
    if speed == 0:
        raise ValueError("speed must be non-zero")
    return math.copysign(abs(speed), distance)
