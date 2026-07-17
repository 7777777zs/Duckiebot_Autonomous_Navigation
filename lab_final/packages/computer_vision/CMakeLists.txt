cmake_minimum_required(VERSION 3.0.2)
project(computer_vision)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  duckietown_msgs
  message_generation
  rospy
  sensor_msgs
  std_msgs
)

add_message_files(
  FILES
  LineDetection.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
    cv_bridge
    duckietown_msgs
    message_runtime
    rospy
    sensor_msgs
    std_msgs
)

catkin_install_python(
  PROGRAMS
    scripts/camera_distortion_node.py
    scripts/camera_processing_node.py
    scripts/color_detection_node.py
    scripts/lane_following_node.py
    scripts/p_controller_node.py
    scripts/pd_controller_node.py
    scripts/pid_controller_node.py
    scripts/state_machine_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
