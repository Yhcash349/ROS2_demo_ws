# blade_demo_basics

ROS Day 3 练习包：创建自己的 ROS2 Python package，包含一个 timer publisher、一个 subscriber 和两个参数。

## Build

```bash
cd /home/yhc23/PROJECT/ROS2_demo_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select blade_demo_basics
source install/setup.bash
```

## Run Nodes Separately

```bash
ros2 run blade_demo_basics status_publisher
ros2 run blade_demo_basics status_subscriber
```

## Launch

```bash
cd /home/yhc23/PROJECT/ROS2_demo_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select blade_demo_basics
source install/setup.bash
ros2 launch blade_demo_basics demo.launch.py
```

## Check

```bash
ros2 node list
ros2 topic info -v /demo/blade_status
ros2 topic echo /demo/blade_status
ros2 param get /status_publisher robot_name
ros2 param get /status_publisher publish_rate
```
