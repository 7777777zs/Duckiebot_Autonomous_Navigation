#!/usr/bin/env python3

import os

import cv2
import rospy
from cv_bridge import CvBridge
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import Image

from computer_vision.detection import detect_colored_line
from computer_vision.msg import LineDetection


class ColorDetectionNode(DTROS):
    """Publish one typed colored-line result for every processed frame."""

    COLORS = ("blue", "red", "green")

    def __init__(self, node_name):
        super().__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        self.vehicle_name = os.environ["VEHICLE_NAME"]
        self.bridge = CvBridge()
        base = f"/{self.vehicle_name}/computer_vision"
        self.detection_pub = rospy.Publisher(f"{base}/line_detection", LineDetection, queue_size=1)
        self.visualization_pub = rospy.Publisher(f"{base}/image/detected", Image, queue_size=1)
        rospy.Subscriber(
            f"{base}/image/processed",
            Image,
            self.image_callback,
            queue_size=1,
        )
        self.log("Color detection node initialized")

    def image_callback(self, msg):
        try:
            image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            results = [detect_colored_line(image, color) for color in self.COLORS]
            result = max(results, key=lambda item: item.area_px)

            detection = LineDetection()
            detection.header = msg.header
            detection.detected = result.detected
            detection.color = result.color
            detection.confidence = result.confidence
            detection.area_px = result.area_px
            detection.distance_cm = result.distance_cm
            detection.x, detection.y, detection.width, detection.height = result.bbox
            self.detection_pub.publish(detection)

            if self.visualization_pub.get_num_connections() > 0:
                visualization = image.copy()
                if result.detected:
                    x, y, width, height = result.bbox
                    cv2.rectangle(visualization, (x, y), (x + width, y + height), (0, 255, 255), 2)
                    cv2.putText(
                        visualization,
                        f"{result.color}: {result.distance_cm:.1f} cm",
                        (10, 24),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2,
                    )
                visualization_msg = self.bridge.cv2_to_imgmsg(visualization, encoding="bgr8")
                visualization_msg.header = msg.header
                self.visualization_pub.publish(visualization_msg)
        except Exception as exc:
            self.logerr(f"Error detecting colors: {exc}")


if __name__ == "__main__":
    ColorDetectionNode(node_name="color_detection_node")
    rospy.spin()
