import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusSubscriber(Node):
    """订阅巡检机器人状态，用来练习 ROS2 subscriber。"""

    def __init__(self):
        super().__init__("status_subscriber")
        self.subscription = self.create_subscription(
            String,
            "blade_status",
            self.status_callback,
            10,
        )
        self.get_logger().info("status_subscriber started, waiting for blade_status messages")

    def status_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
