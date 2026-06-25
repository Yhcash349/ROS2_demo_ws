# RECORD.md

本文件记录 `ROS2_demo_ws` 的每日工程工作复盘，语言应简练，重点服务于以后回溯项目结构、执行过程、验证证据和遗留风险。它不是学习笔记；ROS2/Nav2 概念解释、面试表达、用户问题和原理复盘应写入 `DOCS/NOTE.md`。

当用户要求 Codex “总结今日工作”“今日总结”“记录今天内容”时，Codex 应根据当天当前对话框中的实际工作更新本文件。工程改动、结构调整、配置变化、命令验证、rosbag、图片、CSV、报告、README、Claude 审阅摘要和风险记录写在这里。

## 推荐条目模板

```markdown
## YYYY-MM-DD Day X：任务名称

### 对应计划

说明今天对应 `DOCS/PLAN.md` 的哪个 Stage，以及 `DOCS/ros2_nav2_blade_inspection_20day_plan.md` 的哪一天。如果当天是文档规范、环境修复或计划调整，也要说明和主计划的关系。

### 今日完成

- 简练记录今天实际完成的项目工作。

### 代码、结构与文件改动

- 记录新增、修改、移动或删除了哪些关键代码、文件、配置和目录。
- 说明这些改动对 ROS2 package、launch、参数、地图、数据、报告或文档结构的影响。

### 产物与证据

- 记录当天产生的截图、bag、图片、CSV、map、报告、README、日志或视频等可检查产物。
- 如果产物较大或不适合纳入版本管理，要说明保存位置和处理方式。

### 验证结果

- 记录运行过哪些命令、测试、构建、launch、导航、bag 回放或脚本。
- 写清结果。如果失败，记录关键错误、判断和下一步处理方式。

### Claude 审阅与采纳情况

- 如果今天有 Claude 审阅，记录主要结论、Codex 判断、最终采纳项和暂缓项。
- 如果没有，写“无”即可。

### 待办与风险

- 记录明天或后续需要继续处理的问题、当前未验证部分和计划偏离风险。
```

## 写作规则

`今日完成` 不写泛泛的“学习了 ROS2”，而要写成可追踪结果，例如“完成 `orbit_target.py` 环绕航点生成并输出航点 CSV”。`验证结果` 不写“测试通过”这种空话，而要记录实际命令，例如 `colcon build`、`ros2 launch ...`、`ros2 bag info ...`、`ros2 run ...`、脚本运行命令和结果摘要。

如果当天工作只改文档，也要记录修改了哪些规范和它们如何影响后续执行。如果当天受限于 ROS2 环境、显示服务、Gazebo、依赖下载或硬件条件无法验证，应明确写出“未验证原因”和“剩余风险”。

## 2026-06-13：项目文档规范初始化

### 对应计划

对应 `DOCS/PLAN.md` 的项目初始化与文档体系整理。工作目标是把已有 20 天计划转为主计划，并让 Agent、Record、Note、Claude 审阅规则适配 ROS2/Nav2 风机巡检小验证。

### 今日完成

- 分析已有 `DOCS/ros2_nav2_blade_inspection_20day_plan.md`，明确项目是“导航执行 + 数据采集 + 简单感知评估”的 20 天学习型工程闭环。
- 将通用文档模板改为面向 ROS2/Nav2/Gazebo/风机巡检场景的项目规范。

### 代码、结构与文件改动

- 修改 `AGENTS.md`：增加本项目业务场景、20 天学习取舍、ROS2 工程执行规范、文档记录边界和 Claude 人工中转规则。
- 修改 `DOCS/PLAN.md`：整合 20 天计划，补充业务场景、项目目标、边界、技术选择、目录结构、阶段计划、风险与计划变更记录。
- 继续扩充 `DOCS/PLAN.md`：新增 Day 1-20 每日执行计划，按每天的目标、实用任务、必要概念、产物和降级标准细化路线，降低学习曲线陡峭度。
- 修改 `DOCS/NOTE.md`：定义 ROS2/Nav2 学习笔记模板和写作规则。
- 修改 `DOCS/RECORD.md`：定义工程记录模板，并新增本次文档初始化记录。
- 修改 `CLAUDE.md`：适配本项目的 Claude 审阅入口和 ROS2/Nav2 审阅重点。

### 产物与证据

- 当前产物为项目文档规范、主计划更新和 Day 1-20 每日执行计划扩充，未产生 ROS2 代码、bag、图片或仿真截图。

### 验证结果

- 已阅读 `AGENTS.md`、`CLAUDE.md`、`DOCS/PLAN.md`、`DOCS/NOTE.md`、`DOCS/RECORD.md` 和完整 20 天计划。
- 当前目录不是 Git 仓库，无法使用 `git diff/status` 进行版本差异核对，后续采用文件内容检查验证文档一致性。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 后续进入 Day 1 前，需要实际验证本机 ROS2/Gazebo/Nav2 环境。
- 如果用户希望使用 Git 管理本项目，需要先初始化仓库或迁移到已有仓库。

## 2026-06-13 Day 1：ROS2 环境与 turtlesim 通信入口

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 1：环境与 ROS2 命令行入口。今天目标是确认 ROS2 基础环境可用，并通过 `turtlesim` 建立对 node、topic 和 message 通信的直观认识。

### 今日完成

- 完成 ROS2 安装。
- 启动 `turtlesim` 仿真节点和远程/键盘控制节点。
- 通过控制节点移动小乌龟，观察到两个节点之间通过 ROS2 通信协作。
- 围绕 Node、Message、Topic、Action、Parameter 和 ROS2 在机器人开发中的作用完成 Day 1 学习总结。

### 代码、结构与文件改动

- 未新增 ROS2 代码包。
- 更新 `DOCS/NOTE.md`：新增 Day 1 学习笔记，重点总结 Node、Message、Topic、Action、Parameter 的区别，以及 ROS2 在机器人开发中的作用。
- 更新 `DOCS/RECORD.md`：新增 Day 1 工程记录。

### 产物与证据

- ROS2 环境已安装完成。
- `turtlesim` 已能启动并被远程/键盘控制节点控制移动。
- 今日主要产物是 Day 1 学习笔记和工程记录；未产生 rosbag、截图文件或代码产物。

### 验证结果

- 已通过实际启动 `turtlesim` 和控制节点验证 ROS2 基础通信链路可用。
- 本次记录基于用户已完成的操作描述；Codex 未在当前终端复跑 `ros2 run turtlesim ...`，因此未记录本机命令输出。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- Day 2 需要继续用 `ros2 topic list`、`ros2 topic info -v`、`ros2 service list`、`ros2 action list`、`ros2 param list` 主动观察通信接口。
- 后续建议补充一张 `turtlesim` 运行截图或命令输出，作为 Day 1 可检查证据。

## 2026-06-15 Day 2：ROS2 通信模型与 TurtleSim 观察清单

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 2：ROS2 通信模型。今天目标是继续以 `turtlesim` 为例，观察 topic、service、action、parameter 四类通信接口，并补齐发布/订阅、feedback、result、cancel 和 YAML 参数文件格式的理解。

### 今日完成

- 整理 Day 2 任务清单，明确今日产物应是一页通信机制笔记和至少 10 条 ROS2 CLI 命令。
- 以 `turtlesim` 为例，给出 topic 发布/订阅观察命令，包括 `/turtle1/cmd_vel`、`/turtle1/pose`、`ros2 topic info -v`、`ros2 topic echo` 和 `ros2 topic pub`。
- 以 `turtlesim` 为例，给出 service 请求/响应观察命令，包括 `/spawn`、`/turtle1/set_pen`、`ros2 service list -t`、`ros2 service type` 和 `ros2 service call`。
- 以 `turtlesim` 的 `/turtle1/rotate_absolute` 为例，补充 action 的 goal、feedback、result、cancel 观察方式。
- 补充 parameter 观察和修改命令，包括 `ros2 param list`、`ros2 param get`、`ros2 param set` 和通过 `/clear` 刷新背景颜色。
- 解释 YAML、JSON、TOML 三种配置/数据格式的区别，并说明 ROS2 后续参数文件优先接触 YAML。

### 代码、结构与文件改动

- 未新增 ROS2 package、launch、config、地图、bag 或数据文件。
- 更新 `DOCS/RECORD.md`：新增本 Day 2 工程记录。
- 更新 `DOCS/NOTE.md`：新增 Day 2 学习笔记，记录通信模型、TurtleSim CLI 观察清单、action 关键概念和 YAML/JSON/TOML 区别。

### 产物与证据

- 产物为 Day 2 命令清单、通信模型学习笔记和 YAML 格式说明。
- 当前没有新增截图、rosbag、CSV、地图、图片或代码产物。

### 验证结果

- 本次由 Codex 在文档中整理命令和概念，没有在当前终端实际启动 `turtlesim`、`turtle_teleop_key` 或执行 ROS2 CLI。
- 后续如果用户实际运行命令，建议保存关键终端输出或截图：`ros2 topic list -t`、`ros2 service list -t`、`ros2 action list -t`、`ros2 param list /turtlesim` 和 `/turtle1/rotate_absolute` 的 feedback/result 输出。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- Day 2 仍需用户在本机实际运行上述 TurtleSim 命令，确认 topic、service、action、parameter 的输出和界面变化。
- Day 3 将进入 `ament_python` 练习包创建，需要把今天理解的发布/订阅和 parameter 落到自己的 Python node 中。

## 2026-06-15 Day 3：创建自己的 ROS2 Python 包

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 3：创建自己的 ROS2 Python 包。今天目标是从观察 ROS2 demo 进入自己编写节点，形成 `改代码 -> colcon build -> source -> ros2 run -> 观察输出` 的最小闭环。

### 今日完成

- 在当前项目 workspace `/home/yhc23/PROJECT/ROS2_demo_ws` 下创建了 `src/blade_demo_basics` 练习包。
- 编写 `status_publisher.py`，使用 `rclpy` 创建 `status_publisher` 节点，声明 `robot_name` 和 `publish_rate` 参数，并通过 timer 定时向 `blade_status` topic 发布 `std_msgs/String` 消息。
- 编写 `status_subscriber.py`，创建 `status_subscriber` 节点，订阅同一个 `blade_status` topic 并打印收到的状态消息。
- 在 `setup.py` 中注册两个 console script entry point：`status_publisher` 和 `status_subscriber`。
- 结合代码解释了 `rclpy`、package/node/topic 的区别、`setup.py` entry point 的作用，以及 `main()` 中 `init/spin/destroy_node/shutdown` 的生命周期。

### 代码、结构与文件改动

- 新增 `src/blade_demo_basics/package.xml`：声明包名、`ament_python` 构建类型，以及 `rclpy`、`std_msgs` 依赖。
- 新增 `src/blade_demo_basics/setup.py`：配置 Python 包安装和 `ros2 run` 可执行入口。
- 新增 `src/blade_demo_basics/blade_demo_basics/status_publisher.py`：Day 3 publisher 节点。
- 新增 `src/blade_demo_basics/blade_demo_basics/status_subscriber.py`：Day 3 subscriber 节点。
- 新增 `src/blade_demo_basics/README.md`：记录基本 build 命令；当前 README 仍需补齐 run/check 部分和 Markdown 代码块结尾。
- 当前工作区出现 `build/`、`install/`、`log/`，属于 `colcon build` 生成产物，后续需要通过 `.gitignore` 或版本管理策略避免误提交。

### 产物与证据

- `install/blade_demo_basics/lib/blade_demo_basics/status_publisher` 已生成。
- `install/blade_demo_basics/lib/blade_demo_basics/status_subscriber` 已生成。
- `log/build_2026-06-15_16-38-16/blade_demo_basics/stdout_stderr.log` 显示 `status_publisher.py`、`status_subscriber.py` 被复制到 install 目录，并安装了两个 console script。

### 验证结果

- 已有 `colcon build` 产物和日志证据，说明 `blade_demo_basics` 至少完成了构建与安装步骤。
- Codex 当前没有亲自复跑 `ros2 run blade_demo_basics status_publisher`、`ros2 run blade_demo_basics status_subscriber` 和 `ros2 topic echo /blade_status`，因此双终端运行、topic echo 和参数覆盖仍需最终确认。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 补齐或修正 `src/blade_demo_basics/README.md`，至少包含 publisher/subscriber 运行命令、参数覆盖命令和 topic/param 检查命令。
- 建议运行并保存关键输出：`ros2 node list`、`ros2 topic info -v /blade_status`、`ros2 topic echo /blade_status`、`ros2 param get /status_publisher robot_name`。
- Day 4 将在此基础上增加 launch 文件和 YAML 参数文件，把两个节点组织成一条命令可复现的实验。

## 2026-06-18 Day 4：Launch、参数文件与最小工程组织

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 4：Launch、参数文件与最小工程组织。今天目标是把 Day 3 的 publisher/subscriber 节点从“分别手动运行”整理为“通过一条 launch 命令启动，并从 YAML 加载参数”的可复现实验。

### 今日完成

- 在 `blade_demo_basics` 包内新增 launch/config 组织方式，用 `demo.launch.py` 同时启动 `status_publisher` 和 `status_subscriber`。
- 将 `status_publisher` 的 `robot_name` 和 `publish_rate` 参数写入 `status_demo.yaml`，练习通过 YAML 管理节点运行配置。
- 在 launch 文件中把两个节点的 `blade_status` 都 remap 到 `demo/blade_status`，保证发布端和订阅端仍然对准同一个 topic。
- 修复 `ros2 launch blade_demo_basics demo.launch.py` 报 `file 'demo.launch.py' was not found in the share directory` 的问题。
- 补齐 `src/blade_demo_basics/README.md` 的 Markdown 代码块，并新增 build、单独运行、launch 和检查命令。

### 代码、结构与文件改动

- 新增 `src/blade_demo_basics/launch/demo.launch.py`：使用 `LaunchDescription` 和两个 `Node` action 统一启动 publisher/subscriber。
- 新增 `src/blade_demo_basics/config/status_demo.yaml`：配置 `status_publisher` 的 `robot_name: day4_blade_robot` 和 `publish_rate: 2.0`。
- 修改 `src/blade_demo_basics/setup.py`：补充 `os`、`glob` 导入，并在 `data_files` 中安装 `launch/*.launch.py` 和 `config/*.yaml` 到 package share 目录。
- 修改 `src/blade_demo_basics/README.md`：补充 Day 4 的 `ros2 launch` 复现步骤和 `ros2 topic/param` 检查命令。

### 产物与证据

- `install/blade_demo_basics/share/blade_demo_basics/launch/demo.launch.py` 已生成。
- `install/blade_demo_basics/share/blade_demo_basics/config/status_demo.yaml` 已生成。
- 通过短时间 launch 输出确认两个节点能启动，并且 subscriber 能收到 publisher 的消息。

### 验证结果

- 运行 `colcon build --packages-select blade_demo_basics`，结果为 `1 package finished`。
- 运行 `ROS_LOG_DIR=/tmp/ros_logs ros2 launch blade_demo_basics demo.launch.py --show-args`，launch 文件解析成功，输出 `No arguments`。
- 短时间运行 `ROS_LOG_DIR=/tmp/ros_logs timeout 5s ros2 launch blade_demo_basics demo.launch.py`，验证到：
  - `status_publisher` 和 `status_subscriber` 进程启动。
  - `status_publisher` 使用 YAML 参数启动：`robot_name=day4_blade_robot, publish_rate=2.0`。
  - `status_subscriber` 收到 `/demo/blade_status` 上的消息，例如 `Received: day4_blade_robot status ok, count=0`。
- 当前沙箱环境运行 ROS2 时出现 `getifaddrs: Operation not permitted` 和 UDP socket 权限提示，但节点仍然完成了本地发布/订阅通信。真实用户终端通常不受该沙箱限制。
- 本次验证临时使用 `/tmp/ros_logs` 作为 ROS 日志目录，并在验证后清理。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 用户可在自己的普通终端中重新运行 `ros2 launch blade_demo_basics demo.launch.py`，再用另一个终端检查 `ros2 topic info -v /demo/blade_status` 和 `ros2 param get /status_publisher publish_rate`。
- Day 5 将进入 tf2、坐标系与 RViz，需要从“节点组织和参数管理”过渡到“机器人空间关系和可视化调试”。

## 2026-06-21 Day 5：tf2、坐标系与 RViz

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 5：tf2、坐标系与 RViz。今天目标是理解 `map -> odom -> base_link -> sensor` 坐标树，能用 RViz 显示 TF、LaserScan 和 Image，并能初步判断 frame 缺失、topic 未订阅、坐标树断开等常见问题。

### 今日完成

- 使用 `tf2_ros static_transform_publisher` 手动发布静态坐标变换，搭建最小 tf tree。
- 使用 RViz 显示 Grid、TF、LaserScan 和 Image。
- 使用 `view_frames` 生成 tf 坐标树 PDF。
- 观察到 `/scan` 和 `/image` 话题均有实际数据，并在 RViz 中完成 topic 选择和显示排查。
- 结合 RViz 截图解释了 `map`、`odom`、`base_link`、`camera_frame`、`laser_frame` 或 `single_rrbot_hokuyo_link` 的含义。

### 代码、结构与文件改动

- 今日未新增或修改 ROS2 package 代码。
- 当前正式产物新增 `frames_2026-06-21_21.27.25.pdf`，用于记录 Day 5 tf tree。
- 本次总结更新 `DOCS/RECORD.md` 和 `DOCS/NOTE.md`，分别记录工程证据与学习理解。

### 产物与证据

- `frames_2026-06-21_21.27.25.pdf`：由 `ros2 run tf2_tools view_frames` 生成的 tf tree 图。
- RViz 截图：显示 `Fixed Frame: map`、TF 坐标轴、`LaserScan` display、`Image` display 和图像窗口。
- 终端输出显示当前存在关键 topic：`/tf`、`/tf_static`、`/scan`、`/image`。
- `/scan` 的消息类型为 `sensor_msgs/msg/LaserScan`，实际 `frame_id` 为 `single_rrbot_hokuyo_link`。
- `/image` 的消息类型为 `sensor_msgs/msg/Image`，实际 `frame_id` 为 `camera_frame`，图像尺寸为 `320x240`，编码为 `bgr8`。

### 验证结果

- 运行 `ros2 topic list -t`，确认 `/image [sensor_msgs/msg/Image]`、`/scan [sensor_msgs/msg/LaserScan]`、`/tf [tf2_msgs/msg/TFMessage]`、`/tf_static [tf2_msgs/msg/TFMessage]` 存在。
- 运行 `ros2 topic echo /scan --once`，确认 LaserScan 有数据；其中 `frame_id: single_rrbot_hokuyo_link`。
- 运行 `ros2 topic echo /image --once`，确认 Image 有数据；其中 `frame_id: camera_frame`。
- RViz 初始出现 `Error subscribing: Empty topic name`，判断原因是 `Image` 和 `LaserScan` display 的 `Topic` 为空；将 topic 分别设置为 `/image` 和 `/scan` 后恢复显示。
- `LaserScan` 需要 tf tree 能从 `map` 连到 `single_rrbot_hokuyo_link`；如果只发布了 `base_link -> laser_frame`，则需要补充或改用 `base_link -> single_rrbot_hokuyo_link`。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- Day 6 将进入 Gazebo/TurtleBot 仿真，需要把今天的静态 tf 理解迁移到仿真机器人运动中的动态 `/odom`、`/scan`、`/cmd_vel` 和传感器话题观察。
- 当前 Day 5 使用手动 static transform 搭建教学用坐标树，真实机器人或仿真中 `odom -> base_link` 通常应由里程计、仿真器或状态估计节点动态发布。
- 后续建议保存一张 RViz 截图到计划内报告或数据目录；当前截图来自对话上下文，尚未作为项目文件落盘。

## 2026-06-22 Day 6：Gazebo 仿真与 TurtleBot

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 6：Gazebo 仿真与 TurtleBot。今天目标是启动 TurtleBot/Gazebo 仿真，用键盘遥控机器人，观察 `/cmd_vel`、`/odom`、`/scan`、`/tf` 等关键 topic，并录制一个可回放 rosbag。

### 今日完成

- 启动 TurtleBot3 Gazebo 仿真，并确认当前环境为 ROS2 Jazzy + Gazebo Sim 8。
- 排查 `ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` 报错 `'NoneType' object has no attribute 'lower'` 的问题。
- 确认 Gazebo vendor 版 `gz` 可执行文件位于 `/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz`，并通过补充 `PATH` 和 `GZ_CONFIG_PATH` 使 `gz sim --versions` 正常输出 `8.11.0`。
- 使用 `teleop_keyboard` 遥控仿真机器人，并通过 ROS2 CLI 观察节点、话题、发布者、订阅者和消息内容。
- 在 RViz 中解释如何通过 `Fixed Frame: odom`、`TF`、`RobotModel`、`LaserScan` 显示仿真机器人与雷达数据。
- 录制并回放 Day 6 rosbag，确认 `/cmd_vel`、`/odom`、`/scan`、`/tf`、`/tf_static` 均被写入 bag。

### 代码、结构与文件改动

- 今日未新增或修改 ROS2 package 代码。
- 今日未将 rosbag 纳入项目目录；bag 临时保存在 `/tmp/ros2_day6_bag`，符合大体积数据不直接放入仓库的原则。
- 本次总结更新 `DOCS/RECORD.md` 和 `DOCS/NOTE.md`，分别记录工程证据与学习理解。

### 产物与证据

- 节点观察结果显示当前 ROS2 系统存在：
  - `/robot_state_publisher`
  - `/ros_gz_bridge`
  - `/teleop_keyboard`
- 关键 topic 清单包括：
  - `/cmd_vel [geometry_msgs/msg/TwistStamped]`
  - `/odom [nav_msgs/msg/Odometry]`
  - `/scan [sensor_msgs/msg/LaserScan]`
  - `/tf [tf2_msgs/msg/TFMessage]`
  - `/tf_static [tf2_msgs/msg/TFMessage]`
  - `/robot_description [std_msgs/msg/String]`
- `/cmd_vel` 的发布订阅关系为：`teleop_keyboard` 发布，`ros_gz_bridge` 订阅，说明键盘控制链路已接到 Gazebo bridge。
- `/odom` 和 `/scan` 均由 `ros_gz_bridge` 发布，说明 Gazebo 仿真数据已桥接到 ROS2。
- `/odom` 单条消息中 `frame_id: odom`、`child_frame_id: base_footprint`，机器人位置和速度接近 0，说明当时机器人基本位于起点附近。
- `/scan` 单条消息中 `frame_id: base_scan`，`range_min: 0.12`、`range_max: 3.5`，`ranges` 中同时存在 `.inf` 和具体距离值，说明虚拟雷达能观测到周围障碍物。
- rosbag 产物路径为 `/tmp/ros2_day6_bag/rosbag2_2026_06_22-21_27_14`。
- rosbag 信息：
  - 大小：`4.6 MiB`
  - 存储格式：`mcap`
  - ROS 发行版：`jazzy`
  - 时长：`81.597848024s`
  - 消息总数：`9628`
  - `/cmd_vel`：`836` 条
  - `/odom`：`3505` 条
  - `/scan`：`350` 条
  - `/tf`：`4936` 条
  - `/tf_static`：`1` 条

### 验证结果

- 运行 `ros2 node list`，确认仿真、bridge、键盘遥控相关节点存在。
- 运行 `ros2 topic list -t`，确认 Day 6 需要观察的控制、里程计、雷达和 tf topic 存在。
- 运行 `ros2 topic info -v /cmd_vel`，确认 `/cmd_vel` 存在 1 个 publisher 和 1 个 subscription，分别为 `teleop_keyboard` 和 `ros_gz_bridge`。
- 运行 `ros2 topic info -v /odom` 和 `ros2 topic info -v /scan`，确认两者由 `ros_gz_bridge` 发布。
- 运行 `ros2 topic echo /odom --once` 和 `ros2 topic echo /scan --once`，确认里程计和雷达消息内容合理。
- 运行 `ros2 bag info rosbag2_2026_06_22-21_27_14`，确认 bag 内包含 `/cmd_vel`、`/odom`、`/scan`、`/tf` 和 `/tf_static`。
- 运行 `ros2 bag play rosbag2_2026_06_22-21_27_14`，回放进程正常启动，并在用户停止后输出 `Stopping playback`。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 当前 bag 没有录制 `/robot_description`，因此单独 `ros2 bag play` 时 RViz 可能只能显示 TF 和 LaserScan，完整 RobotModel 仍需要同时提供 `/robot_description` 或重新启动 `robot_state_publisher`。
- 如果后续需要把 Day 6 证据长期保存，应将 `rosbag2_2026_06_22-21_27_14` 转移到计划内数据目录，或只在 `DOCS/RECORD.md` 中保留 `ros2 bag info` 摘要，避免大文件进入版本管理。
- Day 7 将进入 Nav2 第一次导航，需要在今天 Gazebo/TurtleBot 能稳定运行的基础上启动 Nav2 bringup，并观察 AMCL、planner、controller、costmap 和 RViz 目标点导航效果。

## 2026-06-23 Day 7：Nav2 第一次导航

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 7：Nav2 第一次导航。今天目标是从 Day 6 的手动遥控 TurtleBot 进入 Nav2 自主到点：在 RViz 中设置初始位姿和目标点，观察 AMCL、costmap、路径规划、控制输出和 Gazebo 仿真机器人运动。

### 今日完成

- 启动 `nav2_bringup` TurtleBot3 仿真导航示例，进入 RViz + Gazebo + Nav2 联合验证流程。
- 排查 RViz 左下角 `Startup` 灰色不可点的问题，确认 launch 中 lifecycle manager 已自动激活，后续重点应放在 AMCL 初始位姿和 tf 链路。
- 排查终端持续提示 `Frame does not exist` 的问题，定位为 `map -> odom` 尚未由 AMCL 建立；通过 `2D Pose Estimate` 给 AMCL 初始位姿后，`Navigation` 和 `Localization` 均进入 `active`。
- 使用 `tf2_echo odom base_footprint` 与 `tf2_echo map odom` 区分 Gazebo/里程计链路和 AMCL 定位链路：`odom -> base_footprint` 有输出说明仿真机器人位姿链路正常，`map -> odom` 起初缺失说明 AMCL 尚未初始化。
- 排查 RViz `RobotModel` 的 URDF/mesh 加载错误，确认 `/opt/ros/jazzy/share/nav2_minimal_tb3_sim/urdf/turtlebot3_waffle.urdf` 中引用的 `package://nav2_minimal_tb3_sim/models/*.dae` 与实际安装位置 `models/turtlebot3_model/meshes/*.dae` 不一致。
- 修复 `RobotModel` 资源路径问题后，继续通过 RViz `Nav2 Goal` 发送目标点，验证 Nav2 能从 RViz goal 生成路径并控制 Gazebo 中的仿真机器人导航到目标区域。
- 结合今天现象明确 RViz、Gazebo、Nav2 的边界：RViz 负责发送目标和显示状态，Gazebo 负责仿真世界和机器人运动，Nav2 负责定位、建 costmap、规划路径并输出 `/cmd_vel` 速度命令。

### 代码、结构与文件改动

- 今日未新增或修改项目内 ROS2 package 代码。
- 今日修复项发生在 ROS2 系统安装资源层：`nav2_minimal_tb3_sim` 的 TurtleBot3 mesh 资源路径需要与 URDF 引用匹配。该问题属于本机 ROS2 Jazzy 示例包资源路径不一致，不属于 `ROS2_demo_ws` 项目代码问题。
- 本次总结更新 `DOCS/RECORD.md` 和 `DOCS/NOTE.md`，分别记录工程排查过程与学习理解。

### 产物与证据

- RViz 中 `Navigation: active`、`Localization: active`，说明 Nav2 navigation lifecycle 与 AMCL localization 均已激活。
- RViz 中 `Global Status: Ok`，`base_footprint`、`base_link`、`base_scan`、camera 相关 frame 均显示 `Transform OK`。
- 终端日志曾出现 `AMCL cannot publish a pose or update the transform. Please set the initial pose...`，对应初始位姿未设置阶段。
- `tf2_echo odom base_footprint` 能输出连续的 Translation/Rotation，说明 Gazebo/odom 到机器人底盘的 tf 链路正常。
- `tf2_echo map odom` 起初提示 `Invalid frame ID "map"`，说明 AMCL 尚未建立 `map -> odom`；完成 `2D Pose Estimate` 后 RViz localization 转为 active。
- RobotModel 修复前 RViz 报错包括无法加载 `waffle_base.dae`、`lds.dae`、`r200.dae` 和 `tire.dae`。

### 验证结果

- 运行 `ros2 run tf2_ros tf2_echo odom base_footprint`，确认 `odom -> base_footprint` 链路可用。
- 运行 `ros2 run tf2_ros tf2_echo map odom`，确认 `map -> odom` 的缺失与 AMCL 未初始化相关。
- 使用 RViz `2D Pose Estimate` 设置机器人初始位姿后，Nav2 面板显示 `Localization: active`。
- 修复 RobotModel mesh 资源路径后，RViz 中机器人模型可正常显示。
- 使用 RViz `Nav2 Goal` 执行导航目标点验证，Nav2 能生成路径并驱动 Gazebo 仿真机器人移动。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 后续建议保存 Day 7 的 RViz/Gazebo 截图或短视频，作为 3 次到点导航的正式证据。
- Day 8 将进入 Nav2 架构与低风险参数调试，需要在今天的导航链路基础上阅读参数文件，并只修改 `max_vel_x`、`max_vel_theta`、`inflation_radius`、`xy_goal_tolerance` 等低风险参数。
- 当前 RobotModel 修复涉及 `/opt/ros/jazzy` 下系统包资源路径；如果将来换机器或重装 ROS2，可能需要重新检查 `nav2_minimal_tb3_sim` 的 mesh 路径。

## 2026-06-24 Day 8：Nav2 架构与低风险参数调试

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 8：Nav2 架构与低风险参数调试。今天目标是读取 Nav2 参数文件，理解 planner、controller、costmap、goal checker、BT navigator 和 lifecycle manager 的职责，并通过独立参数文件观察速度限制相关配置。

### 今日完成

- 从 ROS2 Jazzy 安装目录复制官方 Nav2 参数文件，建立项目内参数实验文件和原始基线备份。
- 确认当前示例控制器为 MPPI Controller，当前版本的主要速度参数为 `FollowPath.vx_max`、`FollowPath.wz_max`，并确认 `velocity_smoother.max_velocity` 是输出端速度上限。
- 理解并解释 `inflation_radius`、`xy_goal_tolerance`、`vx_max`、`wz_max` 和 `max_velocity` 对路径安全距离、到点判定和运动速度的影响。
- 使用 `ros2 lifecycle nodes`、`ros2 lifecycle get` 和 `/navigate_to_pose` action 状态理解 Nav2 模块的配置、激活与失败传播关系。
- 排查 RViz 地图不显示、Fixed Frame 与 RobotModel 多个 frame 同时报错的问题，确认多个红色 frame 通常是 `map` 或 `map -> odom` 上游链路缺失造成的连锁表现。
- 进一步明确 RViz `2D Pose Estimate` 只负责给 AMCL 设置地图中的初始位置和朝向，不会移动机器人，也不是导航目标。
- 排查自定义参数启动后 `controller_server` 崩溃、导航目标无响应的问题，定位为 `wz_max: 1` 被 YAML 解析为整数，与 MPPI Controller 需要的浮点参数类型不匹配；正确写法应保留小数点，例如 `wz_max: 1.0`。
- 补充理解 Nav2 的框架与插件边界：Planner Server、Controller Server 是提供稳定接口和管理插件的运行平台，NavFn 和 MPPI 分别是当前加载的规划、控制算法插件；costmap layer、Goal Checker、Progress Checker 和恢复行为也可通过插件扩展。
- 明确 Nav2 的价值不只在 lifecycle 管理，还包括模块通信接口、行为树任务组织、地图与代价地图处理、默认算法实现和插件扩展机制。算法可以替换，但必须满足接口、依赖、底盘模型、参数和传感器条件，并重新验证。

### 代码、结构与文件改动

- 新增 `src/blade_inspection_orbit_demo/config/nav2_params.yaml`，作为 Day 8 Nav2 参数实验文件。
- 新增 `src/blade_inspection_orbit_demo/config/nav2_params_original.yaml`，保存复制时的官方参数基线。
- 本次总结更新 `DOCS/RECORD.md` 和 `DOCS/NOTE.md`，分别记录工程事实、故障链和学习理解。
- 当前参数实验文件相对基线的主要变化为：
  - `FollowPath.vx_max`：`0.5 -> 1.0`
  - `FollowPath.wz_max`：`1.9 -> 5.0`
  - `velocity_smoother.max_velocity`：`[0.5, 0.0, 2.0] -> [1.0, 0.0, 4.0]`
  - `velocity_smoother.min_velocity`：`[-0.5, 0.0, -2.0] -> [-1.0, 0.0, -4.0]`

### 验证与排查结果

- 使用 YAML 解析确认 `vx_max: 0.25` 会被解析为浮点数，而 `wz_max: 1` 会被解析为整数，验证了参数类型差异。
- 使用差异检查确认导致 controller 异常的实验修改集中在 MPPI 和 velocity smoother 的速度参数区域，未发现 `inflation_radius` 或 `xy_goal_tolerance` 的实际改动。
- 终端关键错误为：
  - `Lifecycle node controller_server does not have error state implemented`
  - `Failed to change state for node: controller_server`
  - `Failed to bring up all requested nodes. Aborting bringup`
  - `navigate_to_pose action server is not available`
- 故障链为：YAML 参数类型不匹配 -> `controller_server` configure 失败并退出 -> navigation lifecycle bringup 中止 -> `/navigate_to_pose` action 不可用 -> RViz Nav2 Goal 无法触发导航。
- 修正原则已确认：ROS2 浮点参数必须保留浮点写法，例如 `1.0`，不能随意写成整数 `1`。
- 今日未完成对当前高速度实验值 `vx_max: 1.0`、`wz_max: 5.0` 的稳定性和安全性验证，因此不能将其视为推荐配置。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 当前速度参数明显高于 TurtleBot 示例基线，下一次运行前建议恢复基线或改成低速实验值，并一次只修改一组参数。
- 需要重新启动 Nav2，确认 `/map_server`、`/amcl`、`/planner_server`、`/controller_server` 和 `/bt_navigator` 均进入 `active [3]`。
- 需要使用相同初始位姿和目标点完成基线与修改后对比，记录导航时间、速度、转向表现、路径变化和到点结果。
- Day 8 计划中的 `inflation_radius`、`xy_goal_tolerance` 对比实验和 Nav2 模块图尚未形成正式证据，后续可补齐后再进入 Day 9。

## 2026-06-25 Day 9：SLAM 建图与静态地图导航

### 对应计划

对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 9：SLAM 建图与静态地图导航。今天目标是使用 TurtleBot 的 `/scan`、`/odom` 和 tf 数据运行 SLAM，保存自建占据栅格地图，再以静态地图、AMCL 和 Nav2 重新建立定位导航链路。

Day 7 验证的是在 Nav2 示例自带地图上定位和导航；Day 9 增加了“传感器数据 -> SLAM 建图 -> 保存地图 -> 重新加载地图”的工程步骤。今天不是在官方地图上继续编辑，而是对同一个 Gazebo 环境重新采集雷达和里程计数据，独立生成项目自己的地图。

### 今日完成

- 启动 TurtleBot3 Gazebo 仿真和 SLAM Toolbox，使用键盘控制机器人在环境中移动并建立占据栅格地图。
- 使用 `map_saver_cli` 保存 Day 9 自建地图，形成 YAML 元数据与 PGM 栅格图文件。
- 使用保存后的静态地图启动 `map_server` 和 AMCL，验证 `/map` 发布、初始位姿设置以及 `map -> base_footprint` tf 链路。
- 将静态地图启动流程调整为 `autostart:=False`，再按“先 Localization、设置初始位姿、确认 tf、后 Navigation”的顺序手动管理 lifecycle，避免 Planner 在定位完成前激活。
- 验证 localization manager 和 navigation manager 均曾返回 `success=True`。
- 验证 `planner_server`、`bt_navigator`、`velocity_smoother` 和 `collision_monitor` 进入 `active [3]`，并确认 `/navigate_to_pose` 存在由 `/bt_navigator` 提供的 action server。
- 明确 SLAM 建图模式与静态地图导航模式的区别：建图阶段由 SLAM Toolbox 生成 `map -> odom` 和 `/map`；静态导航阶段由 `map_server` 发布已有地图，由 AMCL 根据地图、雷达和里程计建立定位。

### 代码、结构与文件改动

- 新增 `src/blade_inspection_orbit_demo/maps/day9_tb3_map.yaml`。
- 新增 `src/blade_inspection_orbit_demo/maps/day9_tb3_map.pgm`。
- 地图 YAML 当前记录：
  - `resolution: 0.050`
  - `origin: [-0.951, -2.073, 0]`
  - `mode: trinary`
  - `occupied_thresh: 0.65`
  - `free_thresh: 0.196`
- 静态导航继续使用 `src/blade_inspection_orbit_demo/config/nav2_params_original.yaml`，避免 Day 8 尚未验证的高速度实验参数干扰 Day 9。
- 本次总结更新 `DOCS/RECORD.md` 和 `DOCS/NOTE.md`，分别记录工程执行、故障链和学习理解。

### 产物与验证证据

- 地图文件已存在：
  - `src/blade_inspection_orbit_demo/maps/day9_tb3_map.yaml`，约 134 B。
  - `src/blade_inspection_orbit_demo/maps/day9_tb3_map.pgm`，约 12 KiB。
- 静态地图启动后，`map_server` 能发布 `/map [nav_msgs/msg/OccupancyGrid]`，AMCL 和 global costmap 能订阅该地图。
- `ros2 run tf2_ros tf2_echo map base_footprint` 启动瞬间曾提示 `Invalid frame ID "map"`，但随后持续输出 Translation、Rotation 和 Matrix，说明初始位姿生效后完整 tf 链已建立。启动瞬间的一次等待提示不能替代对后续持续输出的判断。
- navigation manager 最终验证返回 `success=True`。
- `/navigate_to_pose` 最终存在 1 个 action server，由 `/bt_navigator` 提供。
- 当前没有形成“在自建地图上完成两个不同目标点导航”的明确日志或截图证据，因此该项不记为已完成。

### 关键故障与处理记录

#### 1. TurtleBot3 teleop 数值变化但机器人不动

现象是 `turtlebot3_teleop` 终端持续显示线速度和角速度变化，但 Gazebo 中机器人没有反应。

检查 ROS 图后发现，当前 Jazzy 仿真最终接收的是 `/cmd_vel [geometry_msgs/msg/Twist]`，而 Jazzy 的 `turtlebot3_teleop` 默认发布 `TwistStamped`。终端数值变化只能证明键盘节点收到了按键，不能证明消息类型和话题已经接入 Gazebo。

处理方式是改用 `teleop_twist_keyboard`，发布非 stamped 的 `Twist`，并将输出 remap 到 Nav2 的输入链：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args \
  -p stamped:=false \
  -r cmd_vel:=cmd_vel_nav
```

对应速度链路为：

```text
teleop -> /cmd_vel_nav -> velocity_smoother
       -> /cmd_vel_smoothed -> collision_monitor
       -> /cmd_vel -> ros_gz_bridge -> Gazebo
```

通用结论是：遥控终端显示速度不等于机器人收到速度；应使用 `ros2 topic info -v` 同时核对 topic 名、message type、publisher 和 subscriber。

#### 2. 静态导航自动启动时 Planner 与 BT Navigator 未激活

现象是 `/map_server`、`/amcl` 和 `/controller_server` 为 `active [3]`，但 `/planner_server`、`/bt_navigator` 为 `inactive [2]`，`/lifecycle_manager_navigation/is_active` 返回 `success=False`。

日志中的关键错误为：

```text
Failed to change state for node: planner_server
Failed to bring up all requested nodes. Aborting bringup.
AMCL cannot publish a pose or update the transform. Please set the initial pose...
```

根因是 localization 与 navigation 同时自动启动时，AMCL 尚未收到初始位姿，`map -> odom -> base_link` 还没有建立。Planner 激活内部 global costmap 时等待全局 tf 超时，导致 navigation lifecycle 在中途终止。

最终采用的稳定顺序是：

```text
autostart:=False
-> 启动 lifecycle_manager_localization
-> 在 RViz 设置 2D Pose Estimate
-> 确认 map -> base_footprint 持续输出
-> 启动 lifecycle_manager_navigation
```

通用结论是：静态地图存在不等于定位已经建立。Planner 的 global costmap 不仅需要 `/map`，还需要机器人能够通过 tf 转换到 `map` 坐标系。

#### 3. 部分节点已 active 时再次执行 STARTUP 失败

在第一次 navigation bringup 部分成功后，直接再次发送 `{command: 0}`，日志出现：

```text
controller_server:
Unable to start transition 1 from current state active:
Transition is not registered.
```

原因是 `STARTUP` 会从管理列表第一个节点重新执行 configure/activate，而 `controller_server` 已经处于 active，不能再次执行 configure transition。不能把 `STARTUP` 当成对失败节点的单独重试。

曾尝试先执行 lifecycle `RESET` 再 `STARTUP`。RESET 返回成功，但随后组合节点容器 `component_container_isolated` 以 `exit code -6` 退出，因此该残缺 launch 被停止并重新启动。

通用结论是：lifecycle manager 出现“部分节点 active、部分 inactive”时，优先重新启动整套 launch 并采用正确启动顺序，不要反复对同一残缺状态执行 STARTUP。

#### 4. `autostart:=False` 后 RViz 没有地图

现象是 Gazebo/RViz 已打开，但 RViz 中没有静态地图。

原因是 `autostart:=False` 不仅阻止 Navigation 自动激活，也会让 `map_server` 和 AMCL 保持未激活；未激活的 `map_server` 不发布 `/map`。这不是地图文件损坏。

处理方式是先调用 localization manager：

```bash
ros2 service call \
  /lifecycle_manager_localization/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes \
  "{command: 0}"
```

另外，`$PWD` 会随命令执行目录变化。若在 `~` 中运行，`map:=$PWD/src/...` 会展开到错误路径。因此后续静态地图与参数文件统一使用绝对路径，或先明确 `cd /home/yhc23/PROJECT/ROS2_demo_ws`。

#### 5. 只有 Gazebo 窗口，没有看到 RViz

`headless:=False` 只控制 Gazebo GUI，不控制 RViz；RViz 由 `use_rviz` 参数控制。日志确认 RViz 进程实际启动过，但 WSLg 下可能出现窗口被遮挡、窗口未正常呈现或随 launch 异常退出。

为降低耦合，后续可使用 `use_rviz:=False` 启动 Gazebo/Nav2，再在独立终端启动：

```bash
ros2 launch nav2_bringup rviz_launch.py use_sim_time:=True
```

通用结论是：Gazebo GUI、RViz 和 Nav2 节点是三个不同部分。某一个窗口存在或缺失，不能直接判断另外两部分是否正常。

#### 6. ROS2 CLI 完全无输出与 Fast DDS 共享内存冲突

多次出现 `ros2 service call` 输入后完全没有 `waiting for service...` 输出，或报：

```text
[RTPS_TRANSPORT_SHM Error]
Failed init_port fastrtps_port7005:
open_and_lock_file failed
```

检查发现旧 `ros2-daemon` 长时间占用 `/dev/shm/fastrtps_port7005`，同时重复执行命令产生了多个卡住的 service call，ROS 图中还曾出现重复的 `/map_server`、`/nav2_container` 名称。

处理过程是停止卡住的 CLI，停止无响应的旧 daemon，确认没有进程继续持有对应文件后，清理仅属于 `port7005` 的 stale Fast DDS 共享内存文件，再重新调用 lifecycle 服务。处理后 localization manager 和 navigation manager 均成功返回 `success=True`。

通用结论是：CLI 完全没有输出时不要连续重复执行。应先 `Ctrl+C`，检查 `ps`、`ros2 daemon` 和 `/dev/shm/fastrtps_*`；清理时只能删除确认属于失效进程的共享内存文件，不能在正常 ROS2 进程仍占用时批量删除。

#### 7. 多行 Shell 命令中的反斜杠后有空格

曾输入：

```bash
ros2 service call \ 
```

反斜杠后存在空格时，它不再是有效的行续接符，可能导致命令被错误拆分。正确规则是 `\` 必须是该行最后一个字符。关键 lifecycle 命令也可以写成单行，减少复制时的空格错误。

### 当前推荐的静态导航启动顺序

启动主进程时使用绝对路径和 `autostart:=False`：

```bash
ros2 launch nav2_bringup tb3_simulation_launch.py \
  slam:=False \
  headless:=False \
  autostart:=False \
  map:=/home/yhc23/PROJECT/ROS2_demo_ws/src/blade_inspection_orbit_demo/maps/day9_tb3_map.yaml \
  params_file:=/home/yhc23/PROJECT/ROS2_demo_ws/src/blade_inspection_orbit_demo/config/nav2_params_original.yaml
```

随后依次执行：

```bash
ros2 service call /lifecycle_manager_localization/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes "{command: 0}"
```

在 RViz 设置 `2D Pose Estimate`，确认 `map -> base_footprint` 后执行：

```bash
ros2 service call /lifecycle_manager_navigation/manage_nodes \
  nav2_msgs/srv/ManageLifecycleNodes "{command: 0}"
```

最后检查：

```bash
ros2 service call /lifecycle_manager_navigation/is_active \
  std_srvs/srv/Trigger '{}'
```

预期返回 `success=True`。

### Claude 审阅与采纳情况

- 无。

### 待办与风险

- 仍需在自建地图上完成至少两个不同目标点的导航，并保存 RViz 路径截图或短视频，满足 Day 9 原计划的正式验收标准。
- 需要记录自建地图的实际质量问题，例如墙体断裂、空洞、重影或定位漂移；当前只有地图文件，没有形成地图质量对比说明。
- Fast DDS 共享内存冲突可能在异常终止 ROS2 进程后复现。后续优先正常关闭 launch 和 CLI，避免反复强制结束进程。
- 当前验证使用 `nav2_params_original.yaml`。Day 8 的高速度实验参数仍未完成稳定性验证，不应切回静态导航主流程。
- 下一步进入 Day 10 前，应先补齐两次目标点导航证据；Day 10 才开始使用 Simple Commander 通过 Python 自动发送单目标。
