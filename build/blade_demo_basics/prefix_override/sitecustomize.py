import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yhc23/PROJECT/ROS2_demo_ws/install/blade_demo_basics'
