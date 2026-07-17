#!/usr/bin/env python3

import os

import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import CameraInfo, CompressedImage, Image
from duckietown.dtros import DTROS, NodeType


class CameraProcessingNode(DTROS):
    """Convert the robot camera stream into one consistent processed image."""

    def __init__(self, node_name):
        super().__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        self.vehicle_name = os.environ["VEHICLE_NAME"]
        self.bridge = CvBridge()
        self.camera_matrix = None
        self.dist_coeffs = None

        namespace = f"/{self.vehicle_name}/computer_vision/image"
        self.undistorted_pub = rospy.Publisher(f"{namespace}/undistorted", Image, queue_size=1)
        self.processed_pub = rospy.Publisher(f"{namespace}/processed", Image, queue_size=1)

        rospy.Subscriber(
            f"/{self.vehicle_name}/camera_node/camera_info",
            CameraInfo,
            self.camera_info_callback,
            queue_size=1,
        )
        rospy.Subscriber(
            f"/{self.vehicle_name}/camera_node/image/compressed",
            CompressedImage,
            self.image_callback,
            queue_size=1,
            buff_size=10_000_000,
        )
        self.log("Camera processing node initialized")

    def camera_info_callback(self, msg):
        self.camera_matrix = np.asarray(msg.K, dtype=np.float32).reshape((3, 3))
        self.dist_coeffs = np.asarray(msg.D, dtype=np.float32)

    def image_callback(self, msg):
        if self.camera_matrix is None or self.dist_coeffs is None:
            return

        try:
            image = self.bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")
            height, width = image.shape[:2]
            new_matrix, _ = cv2.getOptimalNewCameraMatrix(
                self.camera_matrix, self.dist_coeffs, (width, height), 0, (width, height)
            )
            undistorted = cv2.undistort(image, self.camera_matrix, self.dist_coeffs, None, new_matrix)
            processed = cv2.resize(undistorted, (320, 240))
            processed = cv2.GaussianBlur(processed, (5, 5), 0)

            undistorted_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding="bgr8")
            undistorted_msg.header = msg.header
            self.undistorted_pub.publish(undistorted_msg)

            processed_msg = self.bridge.cv2_to_imgmsg(processed, encoding="bgr8")
            processed_msg.header = msg.header
            self.processed_pub.publish(processed_msg)
        except Exception as exc:
            self.logerr(f"Error processing image: {exc}")


if __name__ == "__main__":
    CameraProcessingNode(node_name="camera_processing_node")
    rospy.spin()
