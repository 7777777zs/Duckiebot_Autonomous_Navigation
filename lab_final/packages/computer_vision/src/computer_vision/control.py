"""Controller calculations with explicit fail-safe behavior."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ControllerResult:
    output: float
    integral: float
    derivative: float


def compute_controller_output(
    error,
    previous_error,
    integral,
    dt,
    kp,
    kd,
    ki,
    max_output=8.0,
    max_integral=100.0,
):
    """Return a bounded P/PD/PID output, or zero when input is unsafe."""
    if error is None or dt <= 0:
        return ControllerResult(output=0.0, integral=0.0, derivative=0.0)

    derivative = (error - previous_error) / dt
    next_integral = max(-max_integral, min(max_integral, integral + error * dt))
    output = -(kp * error + kd * derivative + ki * next_integral)
    output = max(-max_output, min(max_output, output))
    return ControllerResult(output=output, integral=next_integral, derivative=derivative)
