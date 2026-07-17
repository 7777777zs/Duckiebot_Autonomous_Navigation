from pathlib import Path


def test_line_detection_message_has_documented_fields():
    message_path = Path(__file__).resolve().parents[1] / "msg" / "LineDetection.msg"
    fields = {
        line.strip()
        for line in message_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }

    assert fields == {
        "std_msgs/Header header",
        "bool detected",
        "string color",
        "float32 confidence",
        "float32 area_px",
        "float32 distance_cm",
        "int32 x",
        "int32 y",
        "int32 width",
        "int32 height",
    }
