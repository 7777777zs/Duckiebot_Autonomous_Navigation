#!/usr/bin/env python3

import os

import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import LEDPattern, Twist2DStamped
from std_msgs.msg import ColorRGBA, String

from computer_vision.msg import LineDetection
from computer_vision.timeouts import is_detection_fresh


class ComputerVisionNode(DTROS):
    """Execute colored-line behavior from typed, time-bounded detections."""

    SEARCHING = "searching"
    APPROACHING = "approaching"
    STOPPING = "stopping"
    TURNING_RIGHT = "turning_right"
    TURNING_LEFT = "turning_left"
    MOVING_STRAIGHT = "moving_straight"
    CONTINUE = "continue"

    def __init__(self, node_name):
        super().__init__(node_name=node_name, node_type=NodeType.PERCEPTION)
        self.vehicle_name = os.environ["VEHICLE_NAME"]
        self.state = self.SEARCHING
        self.state_start_time = rospy.get_time()
        self.last_detection_time = None
        self.detected_color = None
        self.detected_distance = 0.0
        self.detection_timeout = 0.5

        self.stop_duration = 4.0
        self.right_turn_duration = 2.5
        self.left_turn_duration = 2.5
        self.detection_distance = 30.0
        self.stopping_distance = 10.0
        self.normal_speed = 0.22
        self.approach_speed = 0.15
        self.turn_speed = 0.15
        self.straight_distance = 0.3

        base = f"/{self.vehicle_name}"
        self.cmd_vel_pub = rospy.Publisher(
            f"{base}/car_cmd_switch_node/cmd", Twist2DStamped, queue_size=1
        )
        self.led_pattern_pub = rospy.Publisher(
            f"{base}/led_emitter_node/led_pattern", LEDPattern, queue_size=1
        )
        self.state_pub = rospy.Publisher(
            f"{base}/computer_vision/state", String, queue_size=1
        )
        rospy.Subscriber(
            f"{base}/computer_vision/line_detection",
            LineDetection,
            self.detection_callback,
            queue_size=1,
        )
        self.timer = rospy.Timer(rospy.Duration(0.1), self.state_machine_loop)
        rospy.on_shutdown(self.stop_robot)
        self.log("State machine initialized")

    def detection_callback(self, msg):
        self.last_detection_time = rospy.get_time()
        if msg.detected:
            self.detected_color = msg.color
            self.detected_distance = float(msg.distance_cm)
        else:
            self.detected_color = None
            self.detected_distance = 0.0

    def has_fresh_detection(self):
        return is_detection_fresh(
            self.last_detection_time,
            rospy.get_time(),
            self.detection_timeout,
        )

    def set_state(self, state):
        self.state = state
        self.state_start_time = rospy.get_time()

    def set_led_pattern(self, pattern):
        colors = {
            "off": [(0.0, 0.0, 0.0)] * 5,
            "left": [(1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
            "right": [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 0.0), (1.0, 1.0, 0.0)],
            "brake": [(1.0, 0.0, 0.0)] * 5,
        }
        msg = LEDPattern()
        msg.header.stamp = rospy.Time.now()
        for red, green, blue in colors.get(pattern, colors["off"]):
            msg.rgb_vals.append(ColorRGBA(r=red, g=green, b=blue, a=1.0))
        self.led_pattern_pub.publish(msg)

    def publish_command(self, speed, omega):
        command = Twist2DStamped()
        command.v = speed
        command.omega = omega
        self.cmd_vel_pub.publish(command)

    def move_forward(self, speed):
        self.publish_command(speed, 0.0)

    def turn_right(self):
        self.publish_command(self.turn_speed, -3.0)

    def turn_left(self):
        self.publish_command(self.turn_speed, 3.0)

    def stop(self):
        self.publish_command(0.0, 0.0)

    def state_machine_loop(self, _event):
        now = rospy.get_time()
        elapsed = now - self.state_start_time
        self.state_pub.publish(String(data=self.state))

        if self.state == self.SEARCHING:
            if not self.has_fresh_detection() or self.detected_color is None:
                self.stop()
                return
            if self.detected_distance >= self.detection_distance:
                self.set_state(self.APPROACHING)
            else:
                self.stop()

        elif self.state == self.APPROACHING:
            if not self.has_fresh_detection() or self.detected_color is None:
                self.stop()
                self.set_state(self.SEARCHING)
            elif self.detected_distance <= self.stopping_distance:
                self.stop()
                self.set_led_pattern("brake")
                self.set_state(self.STOPPING)
            else:
                self.move_forward(self.approach_speed)

        elif self.state == self.STOPPING and elapsed >= self.stop_duration:
            if self.detected_color == "blue":
                self.set_led_pattern("right")
                self.turn_right()
                self.set_state(self.TURNING_RIGHT)
            elif self.detected_color == "green":
                self.set_led_pattern("left")
                self.turn_left()
                self.set_state(self.TURNING_LEFT)
            elif self.detected_color == "red":
                self.set_led_pattern("brake")
                self.move_forward(self.normal_speed)
                self.set_state(self.MOVING_STRAIGHT)
            else:
                self.stop()
                self.set_state(self.SEARCHING)

        elif self.state == self.TURNING_RIGHT and elapsed >= self.right_turn_duration:
            self.set_led_pattern("off")
            self.move_forward(self.normal_speed)
            self.set_state(self.CONTINUE)

        elif self.state == self.TURNING_LEFT and elapsed >= self.left_turn_duration:
            self.set_led_pattern("off")
            self.move_forward(self.normal_speed)
            self.set_state(self.CONTINUE)

        elif self.state == self.MOVING_STRAIGHT:
            if elapsed >= self.straight_distance / self.normal_speed:
                self.set_led_pattern("off")
                self.move_forward(self.normal_speed)
                self.set_state(self.CONTINUE)
            else:
                self.move_forward(self.normal_speed)

        elif self.state == self.CONTINUE:
            self.move_forward(self.normal_speed)
            if elapsed >= 5.0:
                self.detected_color = None
                self.detected_distance = 0.0
                self.set_state(self.SEARCHING)

    def stop_robot(self):
        self.stop()
        self.set_led_pattern("off")


if __name__ == "__main__":
    ComputerVisionNode(node_name="state_machine_node")
    rospy.spin()
