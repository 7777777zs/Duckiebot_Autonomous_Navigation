cmake_minimum_required(VERSION 3.0.2)
project(computer_vision)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  duckietown_msgs
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS cv_bridge duckietown_msgs rospy sensor_msgs std_msgs
)

catkin_install_python(
  PROGRAMS
    src/camera_distortion_node.py
    src/camera_processing_node.py
    src/color_detection_node.py
    src/lane_following_node.py
    src/p_controller_node.py
    src/pd_controller_node.py
    src/pid_controller_node.py
    src/state_machine_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
