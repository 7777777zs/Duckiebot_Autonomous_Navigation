from computer_vision.control import compute_controller_output


def test_invalid_timestep_stops_controller():
    result = compute_controller_output(2.0, 1.0, 5.0, 0.0, 0.035, 0.01, 0.001)

    assert result.output == 0.0
    assert result.integral == 0.0


def test_integral_term_is_clamped():
    result = compute_controller_output(10.0, 0.0, 99.9, 1.0, 0.0, 0.0, 1.0, max_integral=100.0)

    assert result.integral == 100.0
