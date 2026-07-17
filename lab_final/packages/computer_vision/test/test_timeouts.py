from computer_vision.timeouts import is_detection_fresh


def test_detection_is_fresh_within_timeout():
    assert is_detection_fresh(10.0, 10.4, 0.5) is True


def test_detection_is_stale_after_timeout():
    assert is_detection_fresh(10.0, 10.6, 0.5) is False


def test_missing_detection_timestamp_is_stale():
    assert is_detection_fresh(None, 10.0, 0.5) is False
