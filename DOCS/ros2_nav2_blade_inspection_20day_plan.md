# ROS2/Nav2 风机巡检小验证 20 天实用计划

本文档面向“最短时间熟悉 ROS2、Nav2、机器人感知与规划基础，并做出一个可演示小闭环”的目标。核心不是把 ROS2、Nav2、SLAM、强化学习全部学透，而是在 20 天内完成一个小项目：仿真机器人围绕风机塔筒或叶片观测目标移动，按航点采集图像、位姿和 rosbag，并用一个简单感知脚本做叶片/转盘标记检测或粗略转速估计。

建议环境优先使用 `Ubuntu 24.04 + ROS2 Jazzy + Nav2 + Gazebo Modern`。如果实验室已有 Ubuntu 22.04 或硬件驱动只支持 Humble，则可以改用 `Ubuntu 22.04 + ROS2 Humble`，但同一小组内部应尽量统一发行版，避免每个人的包名、Gazebo 版本和教程路径不同。

最终交付物建议命名为 `blade_inspection_orbit_demo`。它不是完整工业巡检系统，而是一个“导航执行 + 数据采集 + 简单感知评估”的最小闭环，为后续真实机器人、风机叶片检测、主动视角规划和强化学习策略打基础。

## 总体学习曲线

第 1-4 天只解决 ROS2 的基本通信、包、launch 和参数，不碰复杂机器人。第 5-9 天进入 tf、Gazebo、Nav2、SLAM 和参数调试，目标是把官方导航 demo 跑稳。第 10-14 天开始写自己的任务脚本，把导航能力变成“围绕目标采集数据”的项目闭环。第 15-17 天把抽象目标替换成风机巡检叙事，引入简单视觉检测和粗略转速估计。第 18-19 天只做强化学习平台认知，不把 RL 强行塞进主项目。第 20 天只做集成、复现和汇报，不再加新功能。

每天建议 2-4 小时。每一天都必须留下可检查产物：截图、代码、README、参数文件、bag 信息、CSV、图片或简短报告。不要只看教程。

## Day 1：环境与 ROS2 命令行入口

项目位置与意义：这是整个小项目的地基，后续所有导航、采集和感知节点都依赖一个稳定、统一、可复现的 ROS2 环境。

昨日承接：无，从环境搭建开始。

今日主线：安装并确认 ROS2 基础环境可用，跑通最小 demo，建立命令行感觉。

明日铺垫：明天会学习 topic、service、action 和 parameter，今天先知道 ROS2 程序是由多个 node 组成的。

相关基础概念：ROS2 发行版、workspace、node、topic、package、source 环境变量、`ros2` CLI。

今日工作：

- 安装或确认 `Ubuntu 24.04 + ROS2 Jazzy`，如果已有 Humble 环境则记录原因。
- 配置 `source /opt/ros/$ROS_DISTRO/setup.bash`。
- 运行 `turtlesim`，用键盘控制小乌龟。
- 执行并记录 `ros2 node list`、`ros2 topic list`、`ros2 topic echo`、`ros2 run`。
- 建立项目仓库或学习记录目录。

当日交付：`ros2 doctor` 或环境截图、`turtlesim` 截图、一页命令笔记。

## Day 2：ROS2 通信模型

项目位置与意义：这是理解机器人软件“各模块如何说话”的关键，后续相机、里程计、导航目标、任务状态都通过这些通信机制连接起来。

昨日承接：昨天已经能启动 ROS2 程序和查看节点列表，今天解释这些节点之间到底如何通信。

今日主线：搞清 topic、service、action、parameter 的区别，尤其理解为什么导航任务应该用 action。

明日铺垫：明天会自己写第一个 ROS2 包和节点，今天先把通信对象认清楚。

相关基础概念：Topic 发布/订阅、Service 请求/响应、Action 长耗时任务、Parameter 动态配置、message type。

今日工作：

- 跑官方 CLI 教程或等价小例程。
- 用 `ros2 topic info -v` 看话题类型和发布/订阅者。
- 用 `ros2 service list`、`ros2 action list`、`ros2 param list` 理解不同接口。
- 写一段短笔记解释 topic、service、action 的适用场景。
- 明确 Nav2 的“去某个目标点”为什么不是普通 topic。

当日交付：一页通信机制笔记，至少 10 条常用 ROS2 CLI 命令。

## Day 3：创建自己的 ROS2 Python 包

项目位置与意义：这是从“跑别人的 demo”进入“写自己的机器人任务节点”的第一步，后面的图像记录、任务日志和航点控制都要以包的形式组织。

昨日承接：昨天理解了节点通信，今天开始自己创建节点并发布/订阅数据。

今日主线：创建 `ament_python` 包，写 publisher、subscriber、timer 和 parameter 示例。

明日铺垫：明天会把多个节点用 launch 和参数文件组织起来。

相关基础概念：`ros2_ws`、`src`、`ament_python`、`package.xml`、`setup.py`、`colcon build`、Python node。

今日工作：

- 创建 `~/ros2_ws/src` 和一个练习包，例如 `blade_demo_basics`。
- 写一个定时发布状态的 publisher。
- 写一个 subscriber 订阅并打印状态。
- 加入一个 parameter，例如 `robot_name` 或 `publish_rate`。
- 完成 `colcon build` 并 source `install/setup.bash`。

当日交付：一个能编译运行的 ROS2 Python 包，一次 Git 提交。

## Day 4：Launch、参数文件与最小工程组织

项目位置与意义：这是把零散节点变成“别人可以一键复现的实验”的起点，后续项目必须用 launch 启动导航、采集和日志节点。

昨日承接：昨天已经能写单个节点，今天把多个节点和参数组织成可复现实验。

今日主线：学习 `launch.py` 和 YAML 参数文件，形成最小工程结构。

明日铺垫：明天进入 tf、URDF 和 RViz，会看到真实机器人系统比普通节点多了坐标系和可视化。

相关基础概念：LaunchDescription、Node action、参数 YAML、namespace、remap、日志输出。

今日工作：

- 为 Day 3 的两个节点写一个 `demo.launch.py`。
- 把参数从代码默认值移动到 YAML 文件。
- 练习从 launch 里传参、改 topic 名。
- 在 README 中记录启动命令。
- 建立基本目录：`launch/`、`config/`、`scripts/` 或包内模块目录。

当日交付：一条命令可以启动多个练习节点，README 可复现。

## Day 5：tf2、坐标系与 RViz

项目位置与意义：这是机器人导航调试的核心基础；Nav2 失败时，很多问题不是算法错，而是 `map/odom/base_link/sensor` 坐标关系错。

昨日承接：昨天会组织节点和参数，今天学习机器人系统中最重要的“空间关系”。

今日主线：理解 tf tree，知道机器人、雷达、相机、地图坐标之间如何关联。

明日铺垫：明天会进入 Gazebo/TurtleBot 仿真，tf 会从抽象概念变成可视化机器人状态。

相关基础概念：`map`、`odom`、`base_link`、`laser_frame`、`camera_link`、static transform、dynamic transform、RViz display。

今日工作：

- 运行 `robot_state_publisher` 或 TurtleBot 相关示例。
- 用 RViz 显示 RobotModel、TF、LaserScan 或 Image。
- 使用 `tf2_tools view_frames` 生成坐标树。
- 手动画出 `map -> odom -> base_link -> sensor` 的含义。
- 记录常见 tf 错误：frame 不存在、时间戳过期、父子关系断开。

当日交付：`view_frames` 输出图和一页 tf 调试笔记。

## Day 6：Gazebo 仿真与 TurtleBot

项目位置与意义：这是在没有真实机器人时建立低风险试验场，后续风机巡检小验证先在仿真里完成。

昨日承接：昨天理解了坐标系，今天用仿真机器人观察这些坐标系如何随运动变化。

今日主线：启动 TurtleBot 仿真，能在 Gazebo 和 RViz 中观察机器人、传感器和运动。

明日铺垫：明天会启动 Nav2，让机器人从“能动”变成“能自主到目标点”。

相关基础概念：Gazebo、仿真 world、URDF/SDF、差速底盘、里程计、激光雷达、相机话题。

今日工作：

- 安装或确认 TurtleBot/Nav2 示例包。
- 启动 TurtleBot 仿真环境。
- 键盘遥控机器人，观察 `/cmd_vel`、`/odom`、`/scan`。
- 用 `ros2 topic hz` 查看关键话题频率。
- 录制一个短 rosbag 并回放。

当日交付：Gazebo/RViz 截图，一个可回放 rosbag，关键话题清单。

## Day 7：Nav2 第一次导航

项目位置与意义：这是从手动控制进入自主导航的关键节点，后续所有环绕航点和巡检路线都依赖 Nav2 执行目标点。

昨日承接：昨天机器人已经能在仿真中运动，今天把运动交给导航系统。

今日主线：启动 Nav2 bringup，在 RViz 设置初始位姿和目标点，让机器人自动到达。

明日铺垫：明天会拆解 Nav2 内部模块，理解导航失败时应该查哪一层。

相关基础概念：Nav2 bringup、AMCL、global planner、local controller、costmap、goal pose、initial pose。

今日工作：

- 启动 `nav2_bringup` TurtleBot 仿真例程。
- 在 RViz 中设置 `2D Pose Estimate`。
- 发送至少 3 个不同目标点。
- 观察全局路径、局部路径、costmap 和粒子云。
- 记录一次失败案例和解决过程。

当日交付：机器人成功到达 3 个目标点的视频或截图，失败排查记录。

## Day 8：Nav2 架构与参数调试

项目位置与意义：这是把 Nav2 从“黑盒按钮”变成“可调试工程模块”的一天，后续真机低速、安全距离和目标容差都靠参数控制。

昨日承接：昨天已经能让机器人导航，今天理解导航栈由哪些模块组成。

今日主线：认识 planner、controller、costmap、BT navigator，并做几个低风险参数修改。

明日铺垫：明天会做 SLAM 和地图保存，导航会从固定示例地图进入自建地图。

相关基础概念：global costmap、local costmap、inflation layer、obstacle layer、planner server、controller server、behavior tree、goal checker。

今日工作：

- 打开并阅读 Nav2 参数文件的主要部分。
- 修改 `max_vel_x`、`max_vel_theta`、`inflation_radius`、`xy_goal_tolerance`。
- 对比参数修改前后的路径和机器人行为。
- 记录 5 个最常用参数及其作用。
- 保存一份自己的 `nav2_params.yaml`。

当日交付：参数对比记录、`nav2_params.yaml`、一张 Nav2 模块图。

## Day 9：SLAM 建图与静态地图导航

项目位置与意义：这是从“用别人地图导航”过渡到“为自己的测试场景建立地图”，真实巡检前必须有定位和地图流程。

昨日承接：昨天会调 Nav2 参数，今天学习地图从哪里来。

今日主线：用 SLAM 建小地图，保存地图，再用 AMCL 在该地图上导航。

明日铺垫：明天会开始用 Python API 控制 Nav2，为自动航点任务做准备。

相关基础概念：SLAM、occupancy grid、map server、map saver、AMCL、localization、map yaml/pgm。

今日工作：

- 启动 SLAM 模式，遥控机器人绕环境一圈。
- 保存 `map.yaml` 和 `map.pgm`。
- 重新启动静态地图导航。
- 在自建地图上完成至少 2 次目标点导航。
- 记录地图质量问题：空洞、墙体断裂、定位漂移。

当日交付：自建地图文件、导航截图、地图问题记录。

## Day 10：Simple Commander 单目标控制

项目位置与意义：这是把人工 RViz 点目标转换为程序自动发目标，是后续巡检任务自动化的入口。

昨日承接：昨天已经能在地图中导航，今天用 Python 脚本接管“发目标点”这件事。

今日主线：用 `BasicNavigator` 写一个 `go_to_pose_demo.py`，实现单目标导航和结果判断。

明日铺垫：明天会把单目标扩展成多个航点。

相关基础概念：Nav2 action、`BasicNavigator`、`PoseStamped`、feedback、timeout、cancel、TaskResult。

今日工作：

- 写一个脚本设置初始位姿。
- 构造一个 `PoseStamped` 目标点。
- 调用 `goToPose()`。
- 在循环里读取 feedback，加入超时取消逻辑。
- 根据结果输出 succeeded、failed 或 canceled。

当日交付：`go_to_pose_demo.py`，单目标导航日志。

## Day 11：多航点导航

项目位置与意义：这是巡检路径的雏形；真实风机检测不是去一个点，而是按一组观测点依次采集数据。

昨日承接：昨天脚本能发一个目标点，今天扩展成一组目标点。

今日主线：让机器人按 4 个以上航点依次运动，并记录每个航点是否到达。

明日铺垫：明天会把手写航点变成由目标中心和半径自动生成的环绕航点。

相关基础概念：waypoint、`goThroughPoses`、`followWaypoints`、航点状态、任务日志、路径闭环。

今日工作：

- 手写 4 个航点，形成矩形或简单闭环。
- 选择 `goThroughPoses` 或 `followWaypoints` 跑通。
- 为每个航点记录到达时间、结果和误差。
- 在 RViz 中保存路径截图。
- 处理一个失败情形，例如目标不可达或超时。

当日交付：`waypoint_demo.py`，4 航点运行日志和路径截图。

## Day 12：环绕目标航点生成

项目位置与意义：这是风机巡检小项目的任务核心，把“导航能力”转化为“围绕目标观测”的可复用任务模板。

昨日承接：昨天能执行手写航点，今天让航点由任务参数自动生成。

今日主线：输入目标中心、环绕半径、航点数量，生成圆周航点，并让 yaw 始终朝向目标。

明日铺垫：明天会在到达航点后保存相机图像。

相关基础概念：圆周采样、yaw 朝向、四元数、目标中心、观测半径、路径闭环。

今日工作：

- 编写 `orbit_target.py`。
- 参数包括 `center_x`、`center_y`、`radius`、`num_waypoints`、`speed_limit`。
- 生成 8-12 个圆周航点。
- 计算每个航点朝向目标中心的 yaw。
- 让机器人完成一圈并输出任务摘要。

当日交付：`orbit_target.py`，一圈环绕路径截图，航点 CSV。

## Day 13：航点图像采集

项目位置与意义：这是从“机器人会走”转到“机器人为检测任务采数据”，风机叶片检测最终依赖稳定、带位姿的图像序列。

昨日承接：昨天机器人能围绕目标走一圈，今天在每个观测点保存图像。

今日主线：订阅相机图像和相机内参，到达航点后保存图片。

明日铺垫：明天会把图像、位姿、tf、odom 和 rosbag 统一记录成可复现实验数据。

相关基础概念：Image topic、CameraInfo、时间戳、图像编码、cv_bridge、内参、外参。

今日工作：

- 确认仿真相机话题，例如 `/camera/image_raw` 和 `/camera/camera_info`。
- 编写 `image_recorder.py`。
- 到达每个航点后保存 1-3 张图像。
- 保存对应的 `camera_info.yaml` 或内参记录。
- 检查图片命名是否包含航点编号和时间戳。

当日交付：至少 8 个航点的图像、相机内参记录。

## Day 14：位姿、rosbag 与任务日志

项目位置与意义：这是让数据“可复现、可回放、可交给别人处理”的关键，真实机器人实验如果没有 bag 和位姿记录，很难排查和复盘。

昨日承接：昨天已经能按航点保存图像，今天把图像和机器人状态对齐。

今日主线：保存 `pose.csv`，录制 rosbag，并保证图像、位姿、时间戳能互相对应。

明日铺垫：明天会把抽象目标替换成风机巡检场景元素。

相关基础概念：rosbag2、tf、odom、pose、时间同步、CSV 元数据、实验复现。

今日工作：

- 编写 `mission_logger.py`。
- 记录每个航点的目标位姿、实际到达位姿、误差、图片文件名。
- 录制 `/tf`、`/tf_static`、`/odom`、`/scan`、`/cmd_vel`、相机话题。
- 用 `ros2 bag info` 检查 bag 内容。
- 用 `ros2 bag play` 回放一次。

当日交付：`pose.csv`、rosbag、任务日志、回放截图。

## Day 15：风机巡检场景化

项目位置与意义：这是把通用环绕 demo 和老师的风机叶片检测项目接起来，让汇报从“我会 ROS2”变成“我在做风机巡检验证链路”。

昨日承接：昨天完成了环绕采集数据链路，今天替换任务叙事和仿真目标。

今日主线：在仿真中加入简化风机塔筒、轮毂或叶片目标，不追求真实 CAD，只追求可观测。

明日铺垫：明天会在图像中检测叶片、轮毂或标记。

相关基础概念：仿真场景建模、观测目标、检测对象、任务语义、可视化标记。

今日工作：

- 将目标从“树/圆柱”改名为 `wind_turbine_target`。
- 在 Gazebo world 中加入塔筒、轮毂、简化叶片或可旋转标记。
- 调整环绕半径和航点高度/朝向，使相机能看到目标。
- 更新 README 中的项目背景。
- 保存新的场景截图。

当日交付：风机目标仿真场景、更新后的 README、环绕采集截图。

## Day 16：简单视觉检测基线

项目位置与意义：这是感知模块的最小入口，后续真正的叶片缺陷检测、目标识别或视角质量评估都从这里扩展。

昨日承接：昨天已经有风机目标和采集图像，今天开始从图像里提取目标信息。

今日主线：实现一个低成本检测脚本，先检测轮毂、叶片标记或颜色块，不急着上复杂模型。

明日铺垫：明天会用连续图像做粗略转速或运动估计。

相关基础概念：图像坐标、ROI、颜色阈值、轮廓、检测框、置信度、离线处理。

今日工作：

- 从 Day 14/15 的图片中选取一批样例。
- 编写 `detect_blade_marker.py`。
- 可选方案：颜色阈值、AprilTag、简单模板匹配或轻量 YOLO。
- 输出检测框、中心点和可视化结果图。
- 记录失败图片和原因，例如遮挡、模糊、曝光不稳定。

当日交付：检测脚本、可视化检测结果、失败案例记录。

## Day 17：粗略转速或运动估计

项目位置与意义：这是对老师“检测扇叶转速”想法的最低成本回应，不追求工业精度，先验证图像序列能不能产生一个可解释指标。

昨日承接：昨天能在单张图中检测目标，今天把连续帧联系起来估计运动。

今日主线：用连续图像中的标记角度、中心点变化或通过频率估计一个粗略 RPM。

明日铺垫：明天开始看强化学习平台，但 RL 不会替代当前主线闭环。

相关基础概念：帧率、角速度、RPM、时间戳、光流、目标跟踪、离线评估曲线。

今日工作：

- 读取图像序列和时间戳。
- 跟踪叶片标记、轮毂标记或模拟转盘上的颜色块。
- 估计角度变化或周期。
- 输出 RPM 曲线或平均 RPM。
- 写清楚误差来源：帧率、检测失败、运动模糊、视角变化。

当日交付：`rpm_estimator.py` 或 notebook，一张 RPM/运动曲线图。

## Day 18：强化学习最小入门

项目位置与意义：这是为后续主动视角选择、路径策略学习做概念准备，但当前小项目主线仍然是确定性导航和可复现采集。

昨日承接：昨天已经有一个确定性采集和感知闭环，今天只学习 RL 的基本接口，不改动主项目。

今日主线：用 Gymnasium 和 Stable-Baselines3 跑一个 toy env，理解 observation、action、reward、done。

明日铺垫：明天会把 RL 概念映射到机器人巡检任务，但仍只做方案草图。

相关基础概念：environment、observation、action space、reward、episode、PPO、policy、training log。

今日工作：

- 安装或使用已有 Python 环境跑 `CartPole` 或 `LunarLander`。
- 用 Stable-Baselines3 训练一个 PPO baseline。
- 查看训练日志和奖励曲线。
- 写清楚 RL 和普通路径规划的区别。
- 记录为什么不在当前 20 天内训练真实 Nav2 策略。

当日交付：toy RL 训练日志、奖励曲线、RL 基本概念笔记。

## Day 19：机器人 RL 与主动视角规划草图

项目位置与意义：这是把未来论文方向和当前工程闭环连接起来，明确以后哪些部分可能学习，哪些部分继续用规则和 Nav2。

昨日承接：昨天学了 RL 标准接口，今天把这些概念映射到风机巡检。

今日主线：设计一个未来可做的主动视角选择问题，但不急着实现训练。

明日铺垫：明天只做集成复现和汇报，不再扩展新算法。

相关基础概念：next-best-view、coverage、information gain、motion cost、reward design、sim-to-real、Isaac Lab、Gazebo env。

今日工作：

- 定义巡检任务中的 observation：机器人位姿、已观测角度、目标检测质量、剩余未覆盖区域。
- 定义 action：下一个航点、半径调整、视角补拍。
- 定义 reward：覆盖率增加、图像清晰度、运动距离惩罚、安全约束。
- 对比三条路线：规则启发式、Gazebo+Gym 自建环境、Isaac Lab 大规模训练。
- 写一个“未来 1-2 个月扩展路线”草图。

当日交付：机器人 RL/主动视角规划一页方案。

## Day 20：集成、复现与汇报

项目位置与意义：这是把 19 天学习成果收束成一个能展示、能交接、能继续迭代的小项目，而不是停留在零散教程。

昨日承接：昨天已经明确未来扩展方向，今天只验证当前版本是否完整可靠。

今日主线：整理代码、参数、README、视频、bag、图片、CSV 和简短报告，完成一次从零启动复现。

明日铺垫：20 天计划结束后，下一阶段可以进入真机选型、传感器接入、真实场地测试或主动视角策略。

相关基础概念：实验复现、项目交付、README、验收标准、问题清单、版本管理。

今日工作：

- 清理项目结构，保留正式产物，删除无用临时文件。
- 用 README 从零跑一遍：启动仿真、启动 Nav2、执行环绕任务、保存数据、运行检测/转速脚本。
- 录制 3-5 分钟演示视频。
- 写 `day20_summary.md`：做到了什么、没做到什么、下一步风险。
- 准备给老师汇报的 5 页以内材料或提纲。

当日交付：可复现的 `blade_inspection_orbit_demo`、演示视频、summary 报告。

## 推荐最终目录结构

```text
blade_inspection_orbit_demo/
  README.md
  launch/
  config/
    nav2_params.yaml
  maps/
  bags/
  data/
    images/
    pose.csv
    camera_info.yaml
  blade_inspection_orbit/
    orbit_target.py
    image_recorder.py
    mission_logger.py
    detect_blade_marker.py
    rpm_estimator.py
  reports/
    day20_summary.md
```

## 最低验收标准

20 天结束时，不要求你们做出真正能上风场的机器人系统，但必须能证明以下几点：仿真环境能启动；Nav2 能稳定到达目标点；程序能生成并执行环绕航点；每个航点能保存图片和位姿；rosbag 能回放；检测或转速估计脚本能在采集数据上跑出结果；README 能让另一个同学复现。

如果时间不足，优先保证“环绕航点 + 图像/位姿/rosbag 采集 + README 复现”三件事。视觉检测和 RL 可以降级为离线 demo 或方案草图，但不要牺牲主链路稳定性。
