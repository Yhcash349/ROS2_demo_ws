import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share_dir = get_package_share_directory("blade_demo_basics")
    params_file = os.path.join(package_share_dir, "config", "status_demo.yaml")

    return LaunchDescription([
        Node(
            package="blade_demo_basics",
            executable="status_publisher",
            name="status_publisher",
            output="screen",
            parameters=[params_file],
            remappings=[
                ("blade_status", "demo/blade_status"),
            ],
        ),
        Node(
            package="blade_demo_basics",
            executable="status_subscriber",
            name="status_subscriber",
            output="screen",
            remappings=[
                ("blade_status", "demo/blade_status"),
            ],
        ),
    ])