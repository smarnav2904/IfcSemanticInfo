FROM osrf/ros:noetic-desktop-full

SHELL ["/bin/bash", "-c"] 


# required ROS packages  
RUN sudo apt update && apt install -y ros-noetic-joy ros-noetic-teleop-twist-joy \
    ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc \
    ros-noetic-rgbd-launch ros-noetic-rosserial-arduino \
    ros-noetic-rosserial-python ros-noetic-rosserial-client \
    ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server \
    ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro \
    ros-noetic-compressed-image-transport ros-noetic-rqt* ros-noetic-rviz \
    ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers \
    ros-noetic-pcl-conversions ros-noetic-pcl-ros ros-noetic-octomap ros-noetic-octomap-mapping ros-noetic-octomap-msgs ros-noetic-octomap-ros ros-noetic-octomap-rviz-plugins ros-noetic-octomap-server \
    ros-noetic-navigation

# ROS packages for Turtlebot3 robot     
RUN sudo apt install -y ros-noetic-dynamixel-sdk \
    ros-noetic-turtlebot3-*

# we also install Git, just in case
RUN sudo apt install -y git python3-pip
RUN pip install ifcopenshell
RUN pip install lark-parser
RUN sudo apt-get install -y python3-tk
RUN pip install tk
RUN pip install --upgrade matplotlib
RUN sudo apt-get install doxygen


# MESA drivers for hardware acceleration graphics (Gazebo and RViz)
RUN sudo apt -y install libgl1-mesa-glx libgl1-mesa-dri && \
    rm -rf /var/lib/apt/lists/*

# we source the ROS instalation 
RUN source /opt/ros/noetic/setup.bash

# the work directory inside our container
WORKDIR "/home/rva_container"
