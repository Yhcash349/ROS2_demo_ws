import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusPublisher(Node):
    """定时发布巡检机器人状态，用来练习 ROS2 topic 和 parameter。"""

    def __init__(self):
        super().__init__("status_publisher")

        self.declare_parameter("robot_name", "blade_demo_robot")
        self.declare_parameter("publish_rate", 1.0)

        self.robot_name = self.get_parameter("robot_name").value
        publish_rate = float(self.get_parameter("publish_rate").value)
        timer_period = 1.0 / publish_rate if publish_rate > 0 else 1.0

        self.publisher = self.create_publisher(String, "blade_status", 10)
        self.timer = self.create_timer(timer_period, self.publish_status)
        self.count = 0

        self.get_logger().info(
            f"status_publisher started: robot_name={self.robot_name}, publish_rate={publish_rate}"
        )

    def publish_status(self):
        msg = String()
        msg.data = f"{self.robot_name} status ok, count={self.count}"
        self.publisher.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
