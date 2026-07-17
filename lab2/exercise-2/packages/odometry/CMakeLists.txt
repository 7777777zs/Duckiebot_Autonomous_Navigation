cmake_minimum_required(VERSION 3.0.2)
project(odometry)

find_package(catkin REQUIRED COMPONENTS
  duckietown_msgs
  geometry_msgs
  nav_msgs
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS duckietown_msgs geometry_msgs nav_msgs rospy sensor_msgs std_msgs
)

catkin_python_setup()

catkin_install_python(
  PROGRAMS
    src/camera_reader_node.py
    src/move.py
    src/my_publisher_node.py
    src/my_subscriber_node.py
    src/plot.py
    src/template_annotate_image.py
    src/template_D_trajectory.py
    src/wheel_control_node.py
    src/wheel_encoder_reader_node.py
    src/wheel_rotate_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
