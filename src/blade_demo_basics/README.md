# blade_demo_basics

ROS Day 3 练习包：创建自己的 ROS2 Python package，包含一个 timer publisher、一个 subscriber 和两个参数。

## Build

```bash
cd /home/yhc23/PROJECT/ROS2_demo_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select blade_demo_basics
source install/setup.bash
