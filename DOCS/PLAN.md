# PLAN.md

本文件记录 `ROS2_demo_ws` 的项目计划。当前项目不是完整工业级风机巡检系统，而是一个面向学习、演示和后续扩展的小闭环验证：用 ROS2/Nav2/Gazebo 让仿真机器人围绕风机塔筒、轮毂或叶片目标移动，按航点采集图像、位姿和 rosbag，再用简单感知脚本完成叶片/轮毂/标记检测或粗略转速估计。

详细逐日计划保留在 `DOCS/ros2_nav2_blade_inspection_20day_plan.md`。本文件负责把那份 20 天计划收束为项目主计划、边界、阶段目标、目录结构、验证方式和风险管理。

## 用户原始需求与初始化对话摘要

用户希望浏览已有的 ROS2/Nav2 风机巡检 20 天计划，分析整个项目的业务场景和个人学习规划，并按照项目内现有 Markdown 模板，把 Agent 相关规范、`PLAN.md`、`DOCS/RECORD.md` 和 `DOCS/NOTE.md` 改成适合本项目执行的版本。随后用户要求进一步扩充 `PLAN.md` 中每天的计划，具体到 Day 1-20 的日执行层面，并强调学习路线不要过于陡峭，核心目标是尽快熟悉机器人相关设计与开发流程，面向风机巡检业务场景，以实用主义为中心，必要基础概念要覆盖，但不深入不必要的理论分支。

从现有计划可以看出，用户当前目标是最短时间熟悉 ROS2、Nav2、机器人感知与规划基础，同时做出一个可演示小闭环。学习路线强调每天 2-4 小时、每天必须留下可检查产物，不追求一次性学透 ROS2/Nav2/SLAM/RL/工业检测全部内容。

## 项目目标

最终交付一个可复现的 `blade_inspection_orbit_demo`：仿真机器人能在 Gazebo/RViz/Nav2 环境中围绕风机目标执行环绕航点任务，每个航点保存图像和位姿，关键 topic 能录制 rosbag 并回放，离线检测或转速估计脚本能在采集数据上跑出可解释结果，README 能让另一位同学按步骤复现。

最低成功标准如下：仿真环境能启动；Nav2 能稳定到达目标点；程序能生成并执行环绕航点；每个航点能保存图片和位姿；rosbag 能回放；检测或转速估计脚本能在采集数据上跑出结果；README 能说明启动、采集、回放和分析流程。

## 业务场景

业务场景是风机巡检的最小仿真验证。机器人不直接上真实风场，而是在仿真中观察简化风机塔筒、轮毂、叶片或可旋转标记，验证“规划路线、到达观测位、采集数据、离线评估”的基础链路。这个场景服务后续三类扩展：真实机器人和传感器接入，叶片检测/缺陷识别/转速估计，主动视角选择或强化学习策略研究。

当前阶段重点是证明闭环和学习路线成立，而不是追求工业检测精度、真实 CAD 建模、复杂物理仿真、大规模训练或论文级算法指标。

## 项目主旨

本项目以学习型工程项目为主，兼具演示和简历素材价值。执行取舍按以下优先级判断：先保证 ROS2/Nav2 基础链路可运行，再保证数据采集和复现证据完整，然后再做简单视觉检测或转速估计，最后才讨论 RL/主动视角规划。

因此，Codex 和 Claude 审阅时都应避免用完整工业系统标准压垮当前项目，也不应把学习项目写成只有概念没有可运行产物的笔记。每一阶段都应留下代码、命令、截图、bag、CSV、图片、README 或报告等可检查证据。

## 项目边界

当前阶段要做的是 ROS2 基础、Nav2 导航、Gazebo/RViz 仿真、环绕航点生成、图像/位姿/rosbag 采集、简单离线检测或转速估计、README 复现和 20 天总结。

当前阶段不做完整工业风机巡检机器人、不做真实风场部署、不做复杂 CAD/流体/结构仿真、不做高精度缺陷检测模型训练、不做完整 SLAM/定位算法研发、不把 RL 训练并入主闭环、不为早期 demo 引入复杂微服务、数据库或云端平台。

如果时间不足，优先保证“环绕航点 + 图像/位姿/rosbag 采集 + README 复现”三件事。视觉检测和 RL 可以降级为离线 demo 或方案草图，但不能牺牲主链路稳定性。

## 技术选择

推荐环境是 `Ubuntu 24.04 + ROS2 Jazzy + Nav2 + Gazebo Modern`。如果实验室已有 `Ubuntu 22.04 + ROS2 Humble` 或硬件驱动只支持 Humble，可以改用 Humble，但同一小组内部应尽量统一 ROS 发行版、Gazebo 版本和教程路径。

主要技术栈包括 ROS2 CLI、`ament_python`、`rclpy`、launch、YAML 参数、tf2、RViz、Gazebo、TurtleBot/Nav2 示例、Nav2 Simple Commander、rosbag2、OpenCV/cv_bridge、简单图像处理脚本。Day 18-19 可以使用 Gymnasium 和 Stable-Baselines3 认识 RL 接口，但它们不是主项目运行依赖。

验证方式优先使用 `ros2 doctor`、`colcon build`、`ros2 node/topic/service/action/param` CLI、`ros2 launch`、RViz/Gazebo 截图、`tf2_tools view_frames`、`ros2 bag info`、`ros2 bag play`、脚本输出 CSV/图片/曲线和 README 从零复现。

## 目录结构规划

最终项目建议收束为以下结构，早期可以按 Day 逐步生成，不要求一次性建全：

```text
ROS2_demo_ws/
  AGENTS.md
  CLAUDE.md
  DOCS/
    PLAN.md
    RECORD.md
    NOTE.md
    ros2_nav2_blade_inspection_20day_plan.md
  src/
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

`DOCS/` 只放计划、记录和学习笔记。ROS2 package、launch、参数、地图、数据和报告应放入 `src/blade_inspection_orbit_demo/` 或后续实际包目录中。大型 bag、图片集和模型权重是否纳入版本管理，需要在 README 或 `.gitignore` 中单独说明。

## 阶段计划

| 阶段 | 对应天数 | 目标 | 主要产物 | 验证方式 | 是否建议 Claude 审阅 |
| --- | --- | --- | --- | --- | --- |
| Stage 1：ROS2 基础入口 | Day 1-4 | 建立 ROS2 环境、通信模型、Python 包、launch 和参数基础 | 基础练习包、publisher/subscriber、launch、参数 YAML、命令笔记 | `ros2 doctor`、`turtlesim`、`ros2 topic/service/action/param`、`colcon build`、一键 launch | 是，审阅学习路线和包结构 |
| Stage 2：仿真与导航基础 | Day 5-9 | 理解 tf/RViz/Gazebo/Nav2/SLAM，跑稳官方导航 demo 和静态地图导航 | tf tree、Gazebo/RViz 截图、Nav2 参数、地图文件、失败排查记录 | `view_frames`、Gazebo/RViz 运行、Nav2 到点、SLAM 保存地图、静态地图导航 | 是，审阅参数和验证证据 |
| Stage 3：自动航点与数据采集 | Day 10-14 | 用 Simple Commander 发目标，生成环绕航点，保存图像、位姿、rosbag 和任务日志 | `go_to_pose_demo.py`、`waypoint_demo.py`、`orbit_target.py`、`image_recorder.py`、`mission_logger.py`、图像、`pose.csv`、bag | 单目标导航、多航点导航、环绕截图、图片检查、`ros2 bag info/play` | 是，重点审阅主闭环 |
| Stage 4：风机巡检场景与感知基线 | Day 15-17 | 把抽象目标场景化为风机巡检，完成简单检测或粗略转速估计 | 风机目标 world/README、`detect_blade_marker.py`、`rpm_estimator.py`、检测可视化、RPM 曲线 | 采集图像可见目标、检测结果图、失败样例记录、RPM/运动曲线 | 是，审阅业务叙事和算法边界 |
| Stage 5：RL 认知与最终交付 | Day 18-20 | 理解 RL/主动视角方向但不改主闭环，完成项目集成、复现和汇报 | toy RL 日志、主动视角规划草图、README、演示视频、`day20_summary.md` | toy env 日志、README 从零复现、3-5 分钟演示、完整产物清单 | 是，审阅交付完整性和后续路线 |

## 20 天每日执行计划（PLAN 版）

本节是 `DOCS/ros2_nav2_blade_inspection_20day_plan.md` 的主计划版展开。执行原则是先跑通流程，再理解必要概念，最后沉淀可复现产物。每天默认 2-4 小时，不追求把某个方向学透；遇到复杂分支时优先选择能服务风机巡检小闭环的最短路径。每天都应更新 `DOCS/RECORD.md` 的工程证据；如果当天出现关键概念、误解或面试表达，再同步更新 `DOCS/NOTE.md`。

### Day 1：环境与 ROS2 命令行入口

今天只解决“ROS2 能不能跑起来”和“怎么观察 ROS2 系统”。实用任务是确认系统版本、ROS 发行版、`source /opt/ros/$ROS_DISTRO/setup.bash` 是否生效，跑通 `turtlesim` 或等价最小 demo，并用 `ros2 node list`、`ros2 topic list`、`ros2 topic echo` 看见节点和话题。需要理解的概念控制在 ROS2 发行版、workspace、node、topic、package 和环境变量，不展开 DDS、QoS 和底层通信细节。产物是环境记录、最小 demo 截图和 8-10 条常用命令笔记。如果安装受阻，降级目标是把失败命令、系统版本、错误信息和下一步处理写入 `DOCS/RECORD.md`，不要硬卡在复杂环境问题上。

### Day 2：ROS2 通信模型

今天目标是知道机器人模块之间如何传信息。实用任务是用 CLI 观察 topic、service、action、parameter，分别记录它们适合“持续数据流”“一次请求响应”“长耗时任务”“运行参数配置”的场景，并重点理解 Nav2 到点导航为什么适合 action。需要掌握 message type、发布/订阅、请求/响应、feedback/result/cancel 这些必要概念，不深入 DDS QoS 调优。产物是一页通信机制笔记和常用 CLI 清单。降级标准是至少能用自己的话解释相机图像为什么是 topic、导航目标为什么是 action、速度限制为什么适合 parameter。

### Day 3：创建自己的 ROS2 Python 包

今天从跑 demo 进入写自己的节点。实用任务是在工作空间内创建一个 `ament_python` 练习包，例如 `blade_demo_basics`，实现一个 timer publisher、一个 subscriber 和一个简单 parameter，例如 `robot_name` 或 `publish_rate`。需要理解 `src/`、`package.xml`、`setup.py`、entry point、`colcon build` 和 `source install/setup.bash` 的关系，不深入 CMake 或 C++ 包细节。产物是能编译运行的 Python 包、运行命令和一段 README。降级标准是即使节点功能很简单，也必须形成“改代码 -> build -> source -> run -> 观察输出”的闭环。

### Day 4：Launch、参数文件与最小工程组织

今天目标是把零散节点组织成可复现实验。实用任务是为 Day 3 的节点写一个 `demo.launch.py`，把参数移动到 YAML 文件，练习从 launch 传参、修改 topic 名和记录启动命令。需要掌握 `LaunchDescription`、`Node` action、YAML 参数、namespace/remap 的直观用途，不深入 launch 的高级事件和复杂组合。产物是一条命令能启动多个节点的 demo、`launch/` 和 `config/` 目录、README 复现说明。降级标准是至少能做到“别人照 README 可以启动同样节点”。

### Day 5：tf2、坐标系与 RViz

今天进入机器人开发最重要的空间关系，但只学调试必需内容。实用任务是运行 TurtleBot 或 `robot_state_publisher` 示例，在 RViz 里显示 RobotModel、TF、LaserScan 或 Image，用 `view_frames` 生成坐标树，并手画 `map -> odom -> base_link -> sensor` 的含义。需要理解静态 transform、动态 transform、父子坐标系、时间戳，不深入矩阵推导。产物是 tf tree 图、RViz 截图和一页 tf 常见错误笔记。降级标准是能判断 Nav2 报 frame 不存在、时间戳过期、坐标树断开时大概该查哪里。

### Day 6：Gazebo 仿真与 TurtleBot

今天建立低风险试验场。实用任务是启动 TurtleBot/Gazebo 仿真，键盘遥控机器人，观察 `/cmd_vel`、`/odom`、`/scan`、相机话题，用 `ros2 topic hz` 看关键话题频率，并录制一个短 rosbag 回放。需要理解仿真 world、机器人模型、传感器话题、里程计和速度命令的关系，不深入 URDF/SDF 建模。产物是 Gazebo/RViz 截图、关键 topic 清单和可回放 bag。降级标准是如果 Gazebo 图形界面受限，至少记录命令、错误和可替代的 headless 或截图验证方案。

### Day 7：Nav2 第一次导航

今天把机器人从手动控制推进到自主到点。实用任务是启动 Nav2 bringup 示例，在 RViz 设置初始位姿和 2D Goal Pose，让机器人完成至少 3 个目标点导航，并观察全局路径、局部路径、costmap 和粒子云。需要理解 AMCL、planner、controller、costmap、initial pose 和 goal pose 的直观职责，不深入插件实现。产物是 3 次成功到点截图或视频、一次失败排查记录。降级标准是如果不能稳定成功，也要定位失败属于地图/定位/tf/障碍物/参数哪一类。

### Day 8：Nav2 架构与低风险参数调试

今天目标是把 Nav2 从黑盒按钮变成可调试模块。实用任务是阅读参数文件的主要区域，只改低风险参数，例如 `max_vel_x`、`max_vel_theta`、`inflation_radius`、`xy_goal_tolerance`，对比修改前后机器人行为。需要理解 planner server、controller server、global/local costmap、inflation layer、goal checker 和 BT navigator 的大概分工，不深入源码和行为树复杂定制。产物是自己的 `nav2_params.yaml`、5 个常用参数说明和参数对比记录。降级标准是只改 1-2 个参数也可以，但必须说清它们如何影响风机巡检中的低速、安全距离或到点容差。

### Day 9：SLAM 建图与静态地图导航

今天补齐“地图从哪里来”和“如何用地图定位导航”。实用任务是用 SLAM 模式遥控机器人绕小环境，保存 `map.yaml` 和 `map.pgm`，再切换到静态地图 + AMCL 导航，完成至少 2 次目标点。需要理解 occupancy grid、map server、map saver、AMCL、localization 的用途，不深入 SLAM 算法推导。产物是自建地图、静态地图导航截图和地图质量问题记录。降级标准是如果建图效果差，也要记录空洞、墙体断裂、定位漂移等现象和可能原因。

### Day 10：Simple Commander 单目标控制

今天开始把 RViz 手点目标变成程序自动发目标。实用任务是用 `BasicNavigator` 写 `go_to_pose_demo.py`，设置初始位姿，构造 `PoseStamped`，调用 `goToPose()`，读取 feedback，加入 timeout/cancel，最后输出 succeeded、failed 或 canceled。需要理解 Nav2 action、`PoseStamped`、四元数 yaw、feedback、TaskResult，不深入 action server 内部实现。产物是单目标导航脚本和一次运行日志。降级标准是即使目标点固定写死，也要形成“脚本发目标 -> Nav2 执行 -> 脚本判断结果”的闭环。

### Day 11：多航点导航

今天把单目标扩展成巡检路径雏形。实用任务是手写 4 个以上航点，形成矩形或简单闭环，用 `goThroughPoses` 或 `followWaypoints` 跑通，并记录每个航点到达时间、结果和失败原因。需要理解 waypoint、任务日志、路径闭环和不可达目标处理，不深入复杂任务调度。产物是 `waypoint_demo.py`、路径截图和航点运行日志。降级标准是如果多航点 API 卡住，可以先用循环多次 `goToPose()` 实现同样流程，保证学习主线不断。

### Day 12：环绕目标航点生成

今天进入风机巡检任务核心：围绕目标观测。实用任务是编写 `orbit_target.py`，输入目标中心、半径、航点数量和速度限制，生成 8-12 个圆周航点，让 yaw 朝向目标中心，并输出航点 CSV 和任务摘要。需要理解圆周采样、yaw 朝向、目标中心、观测半径和路径闭环，不深入运动规划算法。产物是一圈环绕路径截图、航点 CSV 和可复用脚本。降级标准是先在 2D 平面完成环绕，暂缓高度和复杂相机姿态，避免路线过陡。

### Day 13：航点图像采集

今天让机器人从“会走”变成“为检测任务采数据”。实用任务是确认仿真相机话题和 `CameraInfo`，编写 `image_recorder.py`，在到达航点后保存 1-3 张图片，并保存相机内参记录。需要理解 Image topic、CameraInfo、时间戳、图像编码、cv_bridge 的基本用途，不深入相机标定理论。产物是至少 8 个航点图像、`camera_info.yaml` 或等价记录、图片命名规范。降级标准是如果同步到点触发有困难，可以先手动触发保存图片，但要保留航点编号和时间戳。

### Day 14：位姿、rosbag 与任务日志

今天把数据变成可复现、可回放、可排查的实验材料。实用任务是编写 `mission_logger.py`，记录每个航点的目标位姿、实际到达位姿、误差、图片文件名，同时录制 `/tf`、`/tf_static`、`/odom`、`/scan`、`/cmd_vel` 和相机话题，用 `ros2 bag info` 检查并回放一次。需要理解 rosbag2、pose、odom、tf、时间同步和 CSV 元数据，不深入复杂同步框架。产物是 `pose.csv`、rosbag、任务日志和回放截图。降级标准是只要能让图片、位姿、时间戳三者互相对应，就优先通过。

### Day 15：风机巡检场景化

今天把通用环绕 demo 改成风机巡检叙事。实用任务是将目标命名和 README 背景改为 `wind_turbine_target`，在 Gazebo world 中加入简化塔筒、轮毂、叶片或可旋转标记，调整环绕半径和朝向，让相机能稳定看到目标。需要理解仿真目标、观测对象、任务语义和可视化标记，不追求真实 CAD 和工业物理。产物是风机目标场景、README 背景说明和环绕采集截图。降级标准是先用圆柱、颜色块或简化叶片代替真实模型，只要能支撑后续检测。

### Day 16：简单视觉检测基线

今天只做低成本感知入口，不上来训练复杂模型。实用任务是从采集图片中选样例，编写 `detect_blade_marker.py`，优先使用颜色阈值、轮廓、AprilTag 或模板匹配检测轮毂/叶片标记，输出检测框、中心点和可视化结果图。需要理解图像坐标、ROI、阈值、轮廓、检测框和失败样例，不深入深度学习训练。产物是检测脚本、可视化检测结果和失败案例记录。降级标准是如果真实叶片难检测，就先检测可控颜色块或标记，保证感知链路能跑通。

### Day 17：粗略转速或运动估计

今天验证图像序列能否产生一个可解释运动指标。实用任务是读取连续图片和时间戳，跟踪叶片标记、轮毂标记或模拟转盘颜色块，估计角度变化、通过周期或平均 RPM，并输出曲线。需要理解帧率、角速度、RPM、时间戳、目标跟踪和误差来源，不深入精密运动估计。产物是 `rpm_estimator.py` 或 notebook、RPM/运动曲线和误差说明。降级标准是如果转速估计不稳定，先输出中心点轨迹或角度变化曲线，也算完成“数据到指标”的基础链路。

### Day 18：强化学习最小入门

今天只为后续主动视角规划建立概念，不改主项目闭环。实用任务是用已有 Python 环境或轻量安装跑 `CartPole` 等 toy env，观察 observation、action、reward、episode 和训练日志，写清 RL 和普通路径规划的区别。需要理解 Gymnasium/Stable-Baselines3 的基本接口，不深入算法推导、网络结构和大规模训练。产物是 toy 训练日志、奖励曲线或概念笔记。降级标准是如果环境安装成本高，可以只做代码阅读和接口笔记，不让 RL 阻塞 ROS2 主线。

### Day 19：机器人 RL 与主动视角规划草图

今天把 RL 概念映射到风机巡检未来扩展。实用任务是定义主动视角问题中的 observation、action、reward 和约束，比较规则启发式、Gazebo+Gym 自建环境、Isaac Lab 大规模训练三条路线，并写出未来 1-2 个月路线草图。需要理解 next-best-view、coverage、information gain、motion cost 和 sim-to-real 的直观含义，不实现训练系统。产物是一页主动视角/RL 方案草图。降级标准是只要能说明“当前 20 天为什么不用 RL 替代 Nav2，未来哪些问题可能适合 RL”即可。

### Day 20：集成、复现与汇报

今天停止加新功能，只做收束。实用任务是清理结构，保留正式产物，删除自己确认无用的临时文件，用 README 从零跑一遍启动仿真、启动 Nav2、执行环绕任务、保存数据、回放 bag、运行检测或转速脚本，并录制 3-5 分钟演示视频。需要理解实验复现、验收标准、问题清单和版本管理，不再引入新算法。产物是可复现的 `blade_inspection_orbit_demo`、README、演示视频、`reports/day20_summary.md` 和给老师汇报的 5 页以内提纲。降级标准是如果时间不足，优先保住环绕航点、图像/位姿/rosbag、README 复现三件核心交付。

## 当前确认的约束

当前计划以 20 天、每天 2-4 小时为默认节奏。每一天都需要留下可检查产物，不能只看教程。项目优先使用仿真验证，不依赖真实机器人或真实风机现场。Nav2 和采集主闭环优先级高于视觉算法复杂度和 RL 实现深度。

如果 ROS 发行版在 Jazzy 和 Humble 之间切换，必须记录原因和影响。涉及显示、Gazebo、GPU、系统包安装或网络下载的问题，应把环境限制写入 `DOCS/RECORD.md`，不要把机器问题误写成项目算法问题。

## 风险与待确认问题

- 本机是否已经具备可用的 Ubuntu/ROS2/Gazebo/Nav2 环境尚待实际验证。
- 当前目录还不是 Git 仓库，后续若需要提交记录、分支或 PR，需要先初始化或迁移到版本控制。
- ROS2 Jazzy 与 Humble 的包名、Gazebo 版本和教程路径可能不同，小组需要统一版本。
- Gazebo/RViz 可能受 WSL/显卡/显示服务影响，若无法本地可视化，需要明确替代验证方式。
- 风机目标建模只追求可观测，不追求工业真实度；如果老师要求真实叶片模型，需要单独调整范围。
- 视觉检测和转速估计是低成本 baseline，不能过度包装为高精度工业算法。
- RL/主动视角目前只做概念和未来路线，除非用户明确调整计划，不纳入 20 天主闭环实现。

## 计划变更记录

| 日期 | 变更内容 | 原因 | 是否已确认 |
| --- | --- | --- | --- |
| 2026-06-13 | 将 `DOCS/ros2_nav2_blade_inspection_20day_plan.md` 融入本主计划，明确业务场景、学习主线、阶段计划、边界和验证标准 | 用户要求把现有计划整合进 `PLAN.md`，并让 Agent、Record、Note 规范适配本项目 | 已按用户当前指令执行 |
| 2026-06-13 | 扩充 `PLAN.md` 的 20 天每日执行计划，按每天的目标、实用任务、必要概念、产物和降级标准细化路线 | 用户要求计划具体到每一天，同时保持学习路线平缓、实用主义、面向风机巡检业务场景 | 已按用户当前指令执行 |
