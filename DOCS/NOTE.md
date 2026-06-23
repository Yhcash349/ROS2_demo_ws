# NOTE.md

本文件记录 `ROS2_demo_ws` 的学习笔记，重点服务于 ROS2、Nav2、Gazebo/RViz、tf、SLAM、数据采集、简单视觉检测、转速估计和 RL/主动视角规划的概念理解、原理复盘和面试表达。它不是聊天流水账，也不记录与学习无关的 agent 配置、编辑器杂事或临时操作。

当用户要求 Codex 总结今日学习内容、复盘某一天、解释 ROS2/Nav2 概念或整理八股表达时，应按本文件标准新增或补充当天条目。工程改动、命令验证、文件结构、rosbag、截图和 Claude 审阅摘要主要写入 `DOCS/RECORD.md`；本文件只保留对理解有价值的学习内容。

## 推荐条目模板

同一个项目内标题格式应保持一致，推荐使用：

```markdown
# YYYY-MM-DD Day X：任务名称

## 今日学习位置

说明今天对应 `DOCS/PLAN.md` 的哪一阶段、`DOCS/ros2_nav2_blade_inspection_20day_plan.md` 的哪一天，以及今天在 20 天路线中的作用。

## 今日完成任务

记录当天实际完成的学习产出，例如命令笔记、demo 运行、概念图、脚本阅读、参数理解、截图说明或小实验结果。这里只写和学习理解有关的内容，详细工程文件变动放到 `DOCS/RECORD.md`。

## 基本概念

按难度递进解释当天涉及的核心知识，优先说明“是什么、为什么重要、和当前风机巡检小闭环有什么关系”。

## 项目连接

说明今天学到的概念如何服务后续 `blade_inspection_orbit_demo`，例如 topic 如何连接相机数据，action 为什么适合导航目标，tf 为什么影响 Nav2，rosbag 为什么支持复盘。

## 踩坑记录

记录用户主动暴露的误解、命令/环境/API/编译/仿真问题和解决方式。用户主动问过的问题用红色标注：

<span style="color:red">用户提问：这里写用户问过的问题</span>

## 八股自测

把当天关键知识整理成可口头复述的问答，优先覆盖面试中能讲清楚、并且能和本项目对应起来的内容。

## 明日衔接

用 1-3 句话说明明天会基于今天的内容继续做什么，避免学习路线断裂。
```

## 写作规则

每天最重要知识点使用加粗突出，例如 `**Nav2 的目标导航本质上是一个长耗时 action 任务**`。不要大段复制教程原文；应把概念压缩成用户能复述、能解释给老师或面试官听的表达。

`基本概念` 应优先覆盖当前 Day 需要用到的部分。例如 Day 2 解释 topic、service、action、parameter 的区别；Day 5 解释 `map -> odom -> base_link -> sensor`；Day 10 解释 `BasicNavigator` 和 Nav2 action；Day 14 解释 rosbag、时间戳和位姿对齐；Day 18-19 解释 observation、action、reward、episode 和 next-best-view。

`踩坑记录` 只记录对以后有复用价值的问题，不把每一次普通命令输出都写进去。环境问题要写清楚现象、关键错误、判断过程和解决方式；如果只是工程执行记录，应放入 `DOCS/RECORD.md`。

`八股自测` 应避免空泛定义。每个问答尽量绑定项目例子，例如“为什么导航用 action 而不是 topic？”应回答到 Nav2 到点任务耗时长、需要 feedback、cancel 和 result；“为什么要录 rosbag？”应回答到仿真实验可回放、定位/图像/位姿可复盘。

## 当前学习主线索引

- Day 1-4：ROS2 环境、CLI、通信模型、Python 包、launch、参数。
- Day 5-9：tf2、RViz、Gazebo、TurtleBot、Nav2、参数调试、SLAM、静态地图导航。
- Day 10-14：Simple Commander、单目标、多航点、环绕航点、图像采集、位姿日志、rosbag。
- Day 15-17：风机巡检场景化、简单视觉检测、粗略转速或运动估计。
- Day 18-20：RL/主动视角认知、最终集成、复现和汇报。

# 2026-06-13 Day 1：ROS2 环境与 turtlesim 通信入口

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 1：环境与 ROS2 命令行入口。今天的重点不是写复杂机器人代码，而是先建立对 ROS2 系统的直觉：机器人程序不是一个单体程序，而是一组节点通过标准通信机制协同工作。

## 今日完成任务

今天已经完成 ROS2 安装，并启动了 `turtlesim` 和远程控制/键盘控制相关节点。通过控制小乌龟移动，实际看到了两个节点之间通过 ROS2 通信完成协作：一个节点负责显示和模拟小乌龟状态，另一个节点负责发布控制指令。

这一天最重要的收获是：**ROS2 把机器人系统拆成多个 node，再用 topic、message、action、parameter 等机制把这些模块连接起来**。后续风机巡检项目里的导航、相机、位姿、任务状态和参数配置，本质上都会沿用同一套思路。

## 基本概念

`Node` 是 ROS2 系统里的一个功能单元，可以理解成机器人软件中的一个小模块。一个 node 通常只负责一类事情，例如控制小乌龟、显示仿真界面、发布速度命令、读取相机图像、记录任务日志。机器人项目会有很多 node 同时运行，因为导航、感知、控制、记录不适合全部塞进一个大程序里。

`Message` 是 node 之间传递的数据格式。它规定一条数据里有什么字段、字段类型是什么。例如控制小乌龟移动时，控制节点发出的不是随便一段字符串，而是符合特定消息类型的速度数据。可以把 message 理解成“通信数据的结构说明书”。

`Topic` 是持续数据流的通道。一个 node 可以往某个 topic 发布 message，另一个 node 可以订阅这个 topic 接收 message。turtlesim 里控制节点发布速度命令，仿真节点订阅后让小乌龟移动，这就是 topic 的典型使用场景。后续相机图像、激光雷达、里程计、速度命令通常都会用 topic。

`Action` 用来表示长耗时、需要反馈、可能取消的任务。和 topic 不同，action 不是单纯持续广播数据，而是更像“发起一个任务并等待结果”。例如 Nav2 里的“去某个目标点”不是瞬间完成的，中途需要反馈当前位置、剩余距离，也可能失败或取消，所以导航目标更适合 action。

`Parameter` 是运行时配置。它让 node 的某些行为可以通过外部参数调整，而不是每次都改代码。例如发布频率、机器人名字、最大速度、目标容差、安全距离，都适合做成 parameter。后续 Nav2 参数调试会大量用到这个机制。

这几个概念的区别可以这样记：Node 是干活的模块，Message 是数据格式，Topic 是持续传数据的通道，Action 是长任务接口，Parameter 是模块配置。

## 项目连接

在风机巡检小项目里，ROS2 的价值不是“多一个框架”，而是它提供了一套机器人开发的标准协作方式。导航模块、相机模块、位姿模块、任务脚本、日志模块可以分别写成 node；相机图像、速度命令、里程计可以走 topic；导航到某个巡检航点可以走 action；环绕半径、航点数量、速度限制可以做成 parameter。

这套机制让项目更容易从 `turtlesim` 过渡到 Nav2 和 Gazebo。今天看到的小乌龟移动，本质上就是后续机器人移动的简化版本：控制节点发布运动意图，仿真或机器人节点执行运动，其他节点可以观察状态并记录数据。

ROS2 被机器人开发广泛使用，主要是因为它解决了机器人系统的几个刚需：模块拆分、进程间通信、传感器数据标准化、工具链可视化、参数配置、日志记录和后续仿真/真机迁移。机器人系统通常很复杂，ROS2 让不同模块可以用统一接口连接起来，而不是每个项目都从零发明通信、调试和启动方式。

## 踩坑记录

<span style="color:red">用户提问：Node、Message、Topic、Action、Parameters 这几个有什么差别？ROS2 系统在机器人开发里具体有什么作用，为什么这么多人用？</span>

当前理解重点是先把概念和 turtlesim 现象对应起来，不急着深入 DDS、QoS、Executor、多线程 callback 等底层细节。Day 1 只需要知道 ROS2 程序由多个 node 组成，node 之间通过标准接口协作。

## 八股自测

Q：ROS2 里的 Node 是什么？
A：Node 是一个独立功能模块，负责机器人系统中的某一类任务，例如控制、感知、导航、日志。机器人项目通常由多个 node 协作完成。

Q：Message 和 Topic 的关系是什么？
A：Message 是数据格式，Topic 是传递这种数据的通道。发布者把某种 message 发到 topic，订阅者从 topic 接收这种 message。

Q：为什么控制小乌龟移动可以用 Topic？
A：速度命令是一种持续更新的数据流，控制节点不断发布速度 message，turtlesim 节点订阅后实时更新小乌龟运动，所以适合 topic。

Q：为什么导航到目标点更适合 Action？
A：导航是长耗时任务，需要中途反馈、成功或失败结果，也可能取消。Action 正好支持 goal、feedback、result 和 cancel。

Q：Parameter 有什么用？
A：Parameter 用来配置 node 的行为，例如速度、频率、容差、名称等。它能减少硬编码，让同一个节点适应不同实验条件。

Q：ROS2 为什么在机器人开发里常用？
A：因为机器人系统需要把感知、控制、导航、仿真、记录等模块连接起来。ROS2 提供了节点、通信、参数、launch、工具链和生态包，让开发者能更快搭起可调试、可复用、可扩展的机器人系统。

## 明日衔接

明天可以进入 Day 2：ROS2 通信模型。重点不是背概念，而是用 CLI 主动观察 topic、service、action、parameter 的实际列表和数据类型，进一步把“节点之间怎么说话”这件事看清楚。

# 2026-06-15 Day 2：ROS2 通信模型与 TurtleSim 观察

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 2：ROS2 通信模型。今天的重点是继续用 `turtlesim` 做小实验，把 topic、service、action、parameter 从概念变成可以用命令观察到的接口。

Day 2 在整个风机巡检小项目里的作用是打通“机器人模块之间怎么说话”的直觉。后续相机图像、里程计、速度命令、导航目标、任务状态和 Nav2 参数，本质上都要落到这些 ROS2 通信机制上。

## 今日完成任务

今天整理了 Day 2 的任务清单，并把 `turtlesim` 作为统一例子，拆成四组观察命令：topic 用来观察发布/订阅，service 用来观察请求/响应，action 用来观察 goal、feedback、result 和 cancel，parameter 用来观察运行时配置。

今天还补充理解了 YAML、JSON、TOML 三种常见文本格式的差别。这个问题和 Day 4 的参数文件有关：ROS2 很多参数配置会写在 YAML 文件里，Nav2 后续的速度、容差、安全距离、costmap 等配置也会大量使用 YAML。

## 基本概念

**Topic 是持续数据流，核心是发布/订阅。** 在 `turtlesim` 里，键盘控制节点发布 `/turtle1/cmd_vel`，仿真节点订阅这个 topic 后让小乌龟运动；仿真节点又发布 `/turtle1/pose`，其他节点或命令行可以订阅它来观察位置变化。这个模式适合持续变化的数据，例如速度命令、位姿、相机图像、激光雷达和里程计。

常用观察命令如下：

```bash
ros2 node list
ros2 topic list -t
ros2 topic info -v /turtle1/cmd_vel
ros2 topic info -v /turtle1/pose
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show turtlesim/msg/Pose
ros2 topic echo /turtle1/pose
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}"
```

`ros2 topic info -v` 的重点不是只看 topic 名字，而是看 publisher 和 subscriber。能看懂谁在发布、谁在订阅，才算真正看懂了发布/订阅。

**Service 是一次请求和一次响应。** 在 `turtlesim` 里，`/spawn` 可以请求生成一只新乌龟，`/turtle1/set_pen` 可以请求修改画笔颜色。这类接口适合明确的一次性操作，例如“生成对象”“清屏”“设置画笔”，不适合持续传感器数据，也不适合长时间导航任务。

常用观察命令如下：

```bash
ros2 service list -t
ros2 service type /spawn
ros2 interface show turtlesim/srv/Spawn
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"
ros2 service type /turtle1/set_pen
ros2 interface show turtlesim/srv/SetPen
ros2 service call /turtle1/set_pen turtlesim/srv/SetPen "{r: 255, g: 0, b: 0, width: 3, 'off': 0}"
```

**Action 是长耗时任务接口，核心是 goal、feedback、result 和 cancel。** 在 `turtlesim` 里，`/turtle1/rotate_absolute` 可以让乌龟转到指定角度。发送目标角度是 goal，执行过程中不断返回剩余角度是 feedback，最后返回实际转动结果是 result，任务未完成时中断就是 cancel。

常用观察命令如下：

```bash
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 3.14}" --feedback
```

Nav2 的“去某个目标点”更适合 action，而不是 topic 或 service，因为导航不是瞬间完成的。机器人在路上需要持续反馈状态，可能成功、失败、超时，也可能被用户取消，这正好对应 action 的 feedback、result 和 cancel。

**Parameter 是运行时配置。** 在 `turtlesim` 里，背景颜色就是参数；后续在 Nav2 里，最大速度、目标容差、障碍物膨胀半径、安全距离也会以参数形式出现。parameter 的价值是把可调配置从代码里拿出来，避免每次调参数都改源码。

常用观察命令如下：

```bash
ros2 param list
ros2 param list /turtlesim
ros2 param get /turtlesim background_r
ros2 param set /turtlesim background_r 20
ros2 param set /turtlesim background_g 80
ros2 param set /turtlesim background_b 120
ros2 service call /clear std_srvs/srv/Empty "{}"
```

YAML、JSON、TOML 都是文本格式，用来表达结构化数据。YAML 更像人写的配置文件，靠缩进表达层级，ROS2 参数文件常用它；JSON 更像程序之间交换数据的格式，语法严格，常用于 API 和结构化日志；TOML 更像工具配置文件，常见于 `pyproject.toml`、`Cargo.toml` 等工程配置。

同一个 ROS2 参数例子写成 YAML 是：

```yaml
turtlesim:
  ros__parameters:
    background_r: 20
    background_g: 80
    background_b: 120
```

写成 JSON 是：

```json
{
  "turtlesim": {
    "ros__parameters": {
      "background_r": 20,
      "background_g": 80,
      "background_b": 120
    }
  }
}
```

写成 TOML 是：

```toml
[turtlesim.ros__parameters]
background_r = 20
background_g = 80
background_b = 120
```

当前阶段只需要先掌握 YAML 的三点：缩进表示层级，冒号后面是值，列表用 `-` 表示。后续 Day 4 写 launch 和参数文件时，会真正把 YAML 用到 ROS2 node 上。

## 项目连接

风机巡检小闭环可以直接映射到今天的通信模型。相机图像、激光雷达、机器人位姿和速度命令是持续变化的数据，适合 topic；清空地图、保存地图、触发某个一次性设置更像 service；让机器人去某个巡检航点是长耗时任务，适合 action；巡检半径、航点数量、最大速度、目标容差和安全距离适合 parameter 或 YAML 参数文件。

这也是为什么 Day 2 要先学通信模型，而不是直接写代码。Day 3 创建自己的 Python 包时，至少会写一个 publisher、一个 subscriber 和一个 parameter；Day 10 以后用 Nav2 自动发目标时，会正式接触 action 风格的导航任务。

## 踩坑记录

<span style="color:red">用户提问：计划里提到了发布订阅、feedback、result、cancel，为什么前面的任务清单没有讲？能不能一并给出对应的指令来验证或观察？</span>

补充理解：发布/订阅不是抽象名词，应该用 `ros2 topic info -v` 看 publisher 和 subscriber；feedback、result、cancel 也不是 Nav2 才有，`turtlesim` 的 `/turtle1/rotate_absolute` 就能先观察 action 的基本结构。

<span style="color:red">用户提问：YAML 是什么格式？它和 TOML、JSON 有什么区别？</span>

补充理解：三者都是结构化文本格式。ROS2 当前最需要熟悉 YAML，因为后续参数文件和 Nav2 配置会大量使用 YAML。JSON 更偏程序交换数据，TOML 更偏项目工具配置。

## 八股自测

Q：Topic 的发布/订阅是什么意思？
A：一个节点把 message 发布到 topic，另一个节点订阅这个 topic 接收数据。它适合持续数据流，例如 `/turtle1/cmd_vel`、`/turtle1/pose`、相机图像和里程计。

Q：Service 和 Topic 的区别是什么？
A：Topic 是持续传数据，service 是一次请求和一次响应。`/spawn` 生成乌龟适合 service，但持续发布位姿不适合 service。

Q：Action 里的 feedback、result、cancel 分别是什么？
A：feedback 是任务执行过程中的中间反馈，result 是任务结束后的结果，cancel 是任务未完成时取消它。导航到目标点、旋转到角度这类长耗时任务适合 action。

Q：为什么 Nav2 到点导航不用普通 topic？
A：导航到目标点不是发一次数据就结束，而是一个可能持续几秒到几十秒的任务。中途要反馈进度，最后要报告成功或失败，还要支持取消，所以 action 更合适。

Q：Parameter 和 YAML 参数文件有什么关系？
A：parameter 是节点运行时配置，YAML 是常见的配置文件格式。可以把多个参数写进 YAML，再通过 launch 或命令加载给 ROS2 节点。

Q：YAML、JSON、TOML 怎么区分？
A：YAML 适合人读的层级配置，ROS2 参数常用；JSON 适合程序交换数据，语法严格；TOML 适合工程工具配置，常见写法是 `key = value` 和 `[section]`。

## 明日衔接

明天可以进入 Day 3：创建自己的 ROS2 Python 包。重点是把今天看到的通信机制落到自己的代码里：写一个 timer publisher、一个 subscriber，再加一个简单 parameter，形成“写代码 -> colcon build -> source -> ros2 run -> 观察 topic/param”的闭环。

# 2026-06-15 Day 3：创建自己的 ROS2 Python 包

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 3：创建自己的 ROS2 Python 包。Day 1-2 主要是在 `turtlesim` 和 CLI 中观察别人写好的 ROS2 节点，今天开始把这些概念落到自己的代码里：自己创建 package，自己写 publisher、subscriber 和 parameter。

Day 3 在整个风机巡检小项目中的作用是建立最小代码组织方式。后面的图像采集、任务日志、环绕航点和检测脚本，都不应该只是零散 Python 文件，而应逐步放进 ROS2 package 中，通过 `ros2 run`、launch 和参数文件组织起来。

## 今日完成任务

今天创建了 `blade_demo_basics` 这个 `ament_python` 练习包，并写了两个节点：`status_publisher` 定时向 `blade_status` topic 发布状态消息，`status_subscriber` 订阅同一个 topic 并打印收到的消息。

今天还理解了 `setup.py` 中 `console_scripts` 的作用：它不是简单声明类名，而是把命令行入口和 Python 文件中的 `main()` 函数绑定起来。执行 `ros2 run blade_demo_basics status_publisher` 时，ROS2 最终会找到 `blade_demo_basics.status_publisher:main` 并运行它。

今天最重要的闭环是：**ROS2 package 是工程组织单位，node 是运行起来的功能进程，topic 是节点之间传消息的通道，entry point 是 `ros2 run` 找到 Python 入口的注册表。**

## 基本概念

`rclpy` 是 ROS2 的 Python 客户端库。Python 程序本身不会自动变成 ROS2 节点，必须通过 `rclpy` 初始化 ROS2、创建 node、创建 publisher/subscriber/timer/parameter，并处理回调函数。`from rclpy.node import Node` 让 `StatusPublisher(Node)` 和 `StatusSubscriber(Node)` 继承 ROS2 节点能力。

`blade_demo_basics` 是 package 名，表示今天这个练习包的工程组织单位。它负责放 `package.xml`、`setup.py`、Python 模块和 README。package 本身不是 topic，也不是一个正在运行的节点。

`status_publisher` 和 `status_subscriber` 是通过 `setup.py` 注册出来的可运行命令，同时运行后也分别创建同名 node。它们不是普通意义上的“函数名”。代码里的 `StatusPublisher` 和 `StatusSubscriber` 是类，`main()` 是函数，`status_publisher = blade_demo_basics.status_publisher:main` 是 console script entry point。

`blade_status` 是 topic 名，它不是默认等于包名，而是由代码显式指定的。publisher 中 `create_publisher(String, "blade_status", 10)` 决定发布到这个 topic，subscriber 中 `create_subscription(String, "blade_status", ...)` 决定订阅同一个 topic。两个节点能通信，是因为它们使用了相同 topic 名和相同消息类型 `std_msgs/String`。

`colcon build` 的作用是构建并安装 workspace 里的 ROS2 包。写完代码后，当前终端不会自动知道新包和新入口在哪里，必须通过 `colcon build --packages-select blade_demo_basics` 把包安装到 `install/` 目录，再通过 `source install/setup.bash` 把这个 workspace 的环境加载进当前 shell。每开一个新终端，都要重新 source ROS2 环境和当前 workspace 环境。

`main()` 是 ROS2 Python 节点的运行入口。以 `status_publisher.py` 为例：

```python
def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

`rclpy.init(args=args)` 表示初始化 ROS2 Python 客户端，让这个 Python 进程接入 ROS2 系统。`node = StatusPublisher()` 创建自己定义的节点对象，并执行 `__init__()` 中的参数声明、publisher 创建和 timer 创建。`rclpy.spin(node)` 让节点持续运行并处理 ROS2 事件；对 publisher 来说，它让 timer 周期性触发发布函数，对 subscriber 来说，它让节点持续等待消息并触发 callback。`node.destroy_node()` 用来销毁节点、释放资源。`rclpy.shutdown()` 则关闭当前 Python 进程里的 ROS2 客户端环境。

## 项目连接

今天的 `blade_status` 只是一个练习 topic，但结构和后续风机巡检项目是一样的。之后可以把状态字符串换成任务状态、航点编号、图像保存结果或日志事件；把 `robot_name` 和 `publish_rate` 这种简单参数，换成环绕半径、航点数量、相机保存频率或速度限制。

今天的 package 也为 Day 4 做铺垫。现在 publisher 和 subscriber 需要分别开终端运行，Day 4 会用 launch 文件把多个节点组织起来，并把参数从命令行或代码默认值移动到 YAML 文件中，让别人能用一条命令复现实验。

## 踩坑记录

<span style="color:red">用户提问：`rclpy` 是干啥的？</span>

答：`rclpy` 是 Python 写 ROS2 节点时必须使用的客户端库，负责让 Python 代码接入 ROS2，并提供 node、publisher、subscriber、timer、parameter、spin、shutdown 等接口。

<span style="color:red">用户提问：今天写了一个包，它就是包含一个 Publisher 和一个 Subscriber 吗？默认 topic 是不是这个包的名字？</span>

答：今天写的是一个 package，里面有两个可运行节点，一个发布，一个订阅。topic 不是默认包名，而是代码里显式写的 `blade_status`。包名、节点名、topic 名是三个不同概念。

<span style="color:red">用户提问：`setup.py` 里面声明的是 `statusPublisher` 和 `statusSubscriber` 吗？这应该叫函数吗？</span>

答：`setup.py` 里注册的是 console script entry point。`status_publisher` 是命令名，`blade_demo_basics.status_publisher:main` 指向 Python 模块里的 `main()` 函数。`StatusPublisher` 是类，`main()` 是函数。

<span style="color:red">用户提问：为什么必须 `colcon build`，每次运行前还要 source 工作环境？</span>

答：`colcon build` 把源码包构建并安装到 `install/`，`source install/setup.bash` 把这个 workspace 的包路径和命令入口加载到当前终端。没有 source，`ros2 run` 可能找不到刚写的新包。

<span style="color:red">用户提问：`main()` 里 `rclpy.init`、创建 node、`spin`、`destroy_node`、`shutdown` 分别是干嘛的？</span>

答：这几行分别对应 ROS2 Python 节点的启动、创建节点、持续运行、销毁节点和关闭 ROS2 客户端环境。最关键的是 `spin`，没有它，节点不会持续处理 timer 或 subscriber callback。

## 八股自测

Q：`rclpy` 在 ROS2 Python 节点中起什么作用？
A：`rclpy` 是 ROS2 的 Python 客户端库，负责初始化 ROS2、创建节点、创建通信接口、处理回调和关闭资源。没有它，普通 Python 程序不能作为 ROS2 node 运行。

Q：ROS2 package、node、topic 三者有什么区别？
A：package 是代码和配置的组织单位，node 是运行起来的功能进程，topic 是节点之间传递消息的通道。今天的 package 是 `blade_demo_basics`，节点是 `status_publisher` 和 `status_subscriber`，topic 是 `blade_status`。

Q：`setup.py` 里的 `console_scripts` 有什么用？
A：它把 `ros2 run` 的命令名映射到 Python 模块中的入口函数。例如 `status_publisher = blade_demo_basics.status_publisher:main` 表示运行 `ros2 run blade_demo_basics status_publisher` 时执行 `status_publisher.py` 里的 `main()`。

Q：为什么写完代码后要 `colcon build`？
A：因为 ROS2 workspace 需要把源码包构建并安装到 `install/` 目录，生成可被 `ros2 run` 找到的包索引和可执行入口。只写源码不 build，ROS2 不一定能发现新包。

Q：为什么每个新终端都要 `source install/setup.bash`？
A：source 会把当前 workspace 的环境变量、包路径和命令入口加载进这个终端。新终端默认不知道刚 build 出来的包，所以需要重新 source。

Q：`rclpy.spin(node)` 为什么重要？
A：`spin` 让节点持续运行并处理 ROS2 事件。publisher 的 timer callback、subscriber 的消息 callback 都依赖 `spin` 持续调度；没有 `spin`，节点很快就会退出。

## 明日衔接

明天进入 Day 4：Launch、参数文件与最小工程组织。今天两个节点已经能作为独立命令运行，明天要把它们放进一个 launch 文件中统一启动，并把 `robot_name`、`publish_rate` 这类参数迁移到 YAML 文件里，为后续 Nav2 参数配置打基础。

# 2026-06-18 Day 4：Launch、参数文件与最小工程组织

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 1：ROS2 基础入口，以及 Day 4：Launch、参数文件与最小工程组织。Day 3 已经能分别运行 publisher 和 subscriber，今天的重点是把零散节点组织成一条命令可复现的实验：`ros2 launch blade_demo_basics demo.launch.py`。

Day 4 在整个风机巡检小项目里的作用是建立后续工程组织习惯。之后 Nav2、图像采集、任务日志、rosbag 记录不可能都靠手动开多个终端启动，而应该由 launch 文件统一组织，由 YAML 参数文件管理可调整配置。

## 今日完成任务

今天给 `blade_demo_basics` 增加了 `launch/demo.launch.py` 和 `config/status_demo.yaml`。launch 文件同时启动 `status_publisher` 和 `status_subscriber`，YAML 文件把 `robot_name` 设置为 `day4_blade_robot`，把 `publish_rate` 设置为 `2.0`。

今天还修复了一个典型 ROS2 Python 包问题：源码目录里有 `launch/demo.launch.py`，但 `ros2 launch` 仍然报找不到文件。原因是 `ros2 launch` 查找的是安装后的 package share 目录，不是直接查 `src/`。因此必须在 `setup.py` 的 `data_files` 中声明把 `launch/*.launch.py` 和 `config/*.yaml` 安装进去。

今天最重要的闭环是：**launch 负责统一启动多个节点，YAML 负责外部配置参数，setup.py 负责把 launch/config 等非 Python 文件安装到 ROS2 能找到的位置。**

## 基本概念

`launch` 文件是 ROS2 的启动编排文件。它不负责实现业务逻辑，而是描述“启动哪些节点、节点叫什么、从哪里加载参数、topic 是否改名、日志怎么输出”。今天的 `demo.launch.py` 里有两个 `Node` action，一个启动 `status_publisher`，一个启动 `status_subscriber`。

`LaunchDescription` 可以理解成一份启动清单。`generate_launch_description()` 返回这份清单后，`ros2 launch` 就按照清单创建对应进程。今天的清单里没有复杂事件、条件判断或组合 launch，只保留最小可理解结构。

YAML 参数文件用于把可调配置从代码里移出来。今天的 `status_demo.yaml` 写法是：

```yaml
status_publisher:
  ros__parameters:
    robot_name: "day4_blade_robot"
    publish_rate: 2.0
```

第一层 `status_publisher` 要对应节点名，`ros__parameters` 是 ROS2 参数文件固定字段，下面才是真正的参数名和值。这样做的好处是：要改机器人名字或发布频率时，不需要改 Python 源码，只改配置文件并重新 launch。

`remap` 是启动时改 topic 名。代码里 publisher 和 subscriber 都写的是 `blade_status`，launch 中把两边都 remap 到 `demo/blade_status`。两个节点都要 remap 的原因是：publisher 换了发布频道，subscriber 也必须换到同一个频道听，否则一个发到 `/demo/blade_status`，另一个还在 `/blade_status` 等消息，就无法通信。

`setup.py` 的 `data_files` 不只影响 Python 入口，也影响 launch/config 这类资源文件是否能被 ROS2 找到。`ros2 launch blade_demo_basics demo.launch.py` 查找的是 `install/blade_demo_basics/share/blade_demo_basics/launch/demo.launch.py`。如果 `setup.py` 没有安装 launch 文件，即使源码目录里有这个文件，ROS2 也会报 `file 'demo.launch.py' was not found in the share directory`。

## ROS2 Python 包工作流程总览

一个 ROS2 Python 包可以理解成“把一组机器人功能节点组织起来的工程文件夹”。包本身不是正在运行的程序，而是代码、配置、启动方式和依赖声明的集合；真正运行起来的是包里面的 node。

以当前 `blade_demo_basics` 为例，最小 Python 包主要由这些部分组成：

```text
src/blade_demo_basics/
  package.xml
  setup.py
  setup.cfg
  resource/blade_demo_basics
  blade_demo_basics/
    __init__.py
    status_publisher.py
    status_subscriber.py
  launch/
    demo.launch.py
  config/
    status_demo.yaml
  README.md
```

`package.xml` 是包的身份和依赖说明书。它告诉 ROS2 这个包叫什么、依赖哪些库，例如当前包依赖 `rclpy` 和 `std_msgs`。

`setup.py` 是 Python 包的安装规则。它告诉 `colcon build` 哪些 Python 模块要安装，哪些命令要注册成 `ros2 run` 入口，哪些 launch/config 文件要复制到 install 目录。`console_scripts` 里的 `status_publisher = blade_demo_basics.status_publisher:main` 表示运行 `ros2 run blade_demo_basics status_publisher` 时，执行 `status_publisher.py` 里的 `main()`。

`blade_demo_basics/` 这个 Python 模块目录放真正的节点代码。今天的 `status_publisher.py` 负责定时发布状态消息，`status_subscriber.py` 负责订阅消息并打印。`__init__.py` 用来告诉 Python 这是一个可导入的模块目录。

`resource/blade_demo_basics` 是 ROS2 的包索引标记文件，平时不用改，但它帮助 ROS2 在安装后识别这个包。`launch/` 放启动文件，用来统一启动多个节点、加载 YAML 参数、设置 remap 和输出方式。`config/` 放参数文件，例如 `status_demo.yaml` 管理 `robot_name` 和 `publish_rate`。`README.md` 是给人看的复现说明，应该写清楚怎么 build、source、run、launch 和检查 topic/param。

一个包写好之后，正式运行前通常要经过这几步：

```bash
cd /home/yhc23/PROJECT/ROS2_demo_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select blade_demo_basics
source install/setup.bash
```

`source /opt/ros/jazzy/setup.bash` 是加载系统 ROS2 环境；`colcon build` 是把源码包构建并安装到 `install/`；`source install/setup.bash` 是把当前 workspace 里的包加载到当前终端。每开一个新终端，都要重新 source。

如果只运行单个节点，用 `ros2 run`：

```bash
ros2 run blade_demo_basics status_publisher
ros2 run blade_demo_basics status_subscriber
```

如果要一次启动多个节点，用 `ros2 launch`：

```bash
ros2 launch blade_demo_basics demo.launch.py
```

所以 Day 1-4 的 ROS2 最小工程闭环可以压缩成一句话：`package.xml` 声明依赖，`setup.py` 注册安装和命令入口，Python 文件实现 node，YAML 管参数，launch 统一启动节点，`colcon build` 安装包，`source` 让终端找到包，最后用 `ros2 run` 或 `ros2 launch` 正式运行。

## 项目连接

今天虽然只启动了两个练习节点，但模式已经和后续项目一致。未来风机巡检 demo 中，Nav2 bringup、相机记录、任务日志、环绕航点脚本都需要被统一启动；环绕半径、航点数量、速度限制、目标 topic、保存路径等配置也应该放进 YAML，而不是散落在代码里。

今天的 `demo/blade_status` 可以看作未来任务状态 topic 的雏形。之后它可以扩展成“当前航点编号、采集状态、任务是否完成、图像保存结果”等信息。launch 和 YAML 的价值，就是让这些节点和配置能被别人复现，而不是只在自己当前终端里临时跑通。

## 踩坑记录

<span style="color:red">用户提问：两个节点都要 remap 是干啥？</span>

答：remap 是启动时把代码里的 topic 名换成新 topic 名。publisher 和 subscriber 必须对准同一个 topic 才能通信。如果只 remap publisher，它会发到 `/demo/blade_status`，subscriber 仍然听 `/blade_status`，两边就错开了。所以两个节点都要 remap 到同一个新名字。

<span style="color:red">用户遇到：`ros2 launch blade_demo_basics demo.launch.py` 报 `file 'demo.launch.py' was not found in the share directory`。</span>

原因：`setup.py` 只安装了 `package.xml`，没有安装 `launch/*.launch.py` 和 `config/*.yaml`。修复方式是在 `data_files` 里加上 launch/config 的安装规则，然后重新 `colcon build` 和 `source install/setup.bash`。

补充踩坑：Codex 沙箱里运行 ROS2 launch 时，默认写 `~/.ros/log` 会遇到只读文件系统，所以验证时临时设置了 `ROS_LOG_DIR=/tmp/ros_logs`。这属于当前 agent 沙箱限制，不是项目代码问题。

## 八股自测

Q：ROS2 launch 文件解决什么问题？
A：它把多个节点、参数文件、topic remap 和输出方式组织到一起，让实验可以用一条命令复现，而不是手动开多个终端分别运行。

Q：为什么参数要放进 YAML？
A：YAML 让节点配置独立于代码。比如 `robot_name`、`publish_rate` 后续可以换成环绕半径、航点数量、速度限制和保存路径，这些都适合配置化。

Q：`ros2 launch` 为什么找的是 install/share 目录？
A：ROS2 运行时查找的是已安装 package 的资源目录。源码里的文件只有被 `setup.py` 安装到 `install/.../share/<package>/` 后，`ros2 launch` 才能按 package 名找到它。

Q：remap 和改代码里的 topic 名有什么区别？
A：改代码是固定修改节点默认行为；remap 是启动时临时改名，同一个节点可以在不同实验里接到不同 topic 上，更灵活，也更适合 launch 组织。

Q：为什么 publisher 和 subscriber 要同时 remap？
A：topic 通信要求发布端和订阅端名字一致。只改一边会导致两边处在不同 topic 上，subscriber 收不到 publisher 的消息。

## 明日衔接

明天进入 Day 5：tf2、坐标系与 RViz。今天解决的是“如何组织和启动节点”，明天开始理解机器人系统里的空间关系，也就是 `map -> odom -> base_link -> sensor` 这些坐标系如何影响可视化和导航调试。

# 2026-06-21 Day 5：tf2、坐标系与 RViz

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 5：tf2、坐标系与 RViz。Day 1-4 主要解决 ROS2 节点、通信、package、launch 和参数组织，今天开始进入机器人系统最核心的空间关系：机器人、地图、雷达、相机之间到底如何在同一个空间里对齐。

Day 5 在风机巡检小项目里的作用非常关键。后续机器人围绕风机移动、相机采集图像、雷达避障、Nav2 做路径规划，都需要知道机器人本体和传感器在地图里的位置。如果 tf tree 断了，很多时候不是算法错，而是系统根本不知道数据该放到空间中的哪里。

## 今日完成任务

今天使用 `tf2_ros static_transform_publisher` 手动发布了几条静态坐标变换，搭建出类似 `map -> odom -> base_link -> camera_frame / laser_frame` 的最小坐标树。随后用 `tf2_tools view_frames` 生成了 `frames_2026-06-21_21.27.25.pdf`，用 RViz 显示了 Grid、TF、LaserScan 和 Image，并排查了 RViz 中 `Error subscribing: Empty topic name` 的问题。

今天还通过 `ros2 topic list -t`、`ros2 topic echo /scan --once` 和 `ros2 topic echo /image --once` 确认了 `/scan` 和 `/image` 都有真实数据。`/scan` 的 frame 是 `single_rrbot_hokuyo_link`，`/image` 的 frame 是 `camera_frame`。这说明 RViz 显示传感器数据时，不能只看 topic 是否存在，还要看消息里的 `frame_id` 能不能接入 tf tree。

今天最重要的收获是：**topic 负责传感器或状态数据，tf 负责说明这些数据来自哪个空间坐标，RViz 负责把 topic 和 tf 合起来可视化。**

## 基本概念

`tf2` 是 ROS2 中管理坐标变换的系统。机器人开发里，每个对象或传感器都有自己的坐标系：地图有地图坐标，机器人身体有本体坐标，相机有相机坐标，雷达有雷达坐标。tf2 要解决的问题是：在某个时间点，A 坐标系相对于 B 坐标系在哪里、朝向如何。

`map` 是全局地图坐标系。它通常表示环境中比较稳定的全局参考，例如一张 SLAM 地图或静态地图。Nav2 里全局路径、目标点和 AMCL 定位通常都会围绕 `map` 展开。

`odom` 是里程计坐标系。它通常比较连续，不会突然跳变，但长期可能漂移。真实机器人移动时，`odom -> base_link` 往往由轮速计、仿真器、里程计或状态估计节点动态发布。

`base_link` 是机器人本体坐标系，可以理解成机器人身体中心或底盘中心。后续 Nav2 判断机器人当前位置、控制机器人运动、计算传感器安装位置时，都会围绕 `base_link` 展开。

`camera_frame`、`laser_frame` 或 `single_rrbot_hokuyo_link` 是传感器坐标系。它们描述相机或雷达安装在机器人身体的哪个位置、朝哪个方向。传感器发出的数据只知道自己坐标系下的含义，系统必须通过 tf 才能把这些数据放到 `map` 或 `base_link` 里。

`static_transform_publisher` 用来发布静态坐标关系。比如相机固定安装在机器人前方，这种 `base_link -> camera_frame` 关系不会随机器人运动改变，适合用 static transform 表达。今天为了教学，也把 `map -> odom` 和 `odom -> base_link` 手动写成静态关系；但真实机器人中，`odom -> base_link` 通常是动态的。

下面这条命令表示：在 `odom` 坐标系里，`base_link` 位于 `(1.0, 0.5, 0)`，并且绕 Z 轴转了 `0.3` 弧度。

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 1.0 --y 0.5 --z 0 \
  --roll 0 --pitch 0 --yaw 0.3 \
  --frame-id odom \
  --child-frame-id base_link
```

其中 `--frame-id odom` 是父坐标系，也就是参考系；`--child-frame-id base_link` 是子坐标系，也就是被描述的位置对象。`--x --y --z` 是平移量，单位是米；`--roll --pitch --yaw` 是旋转量，单位是弧度。地面移动机器人最常看的通常是 `yaw`，也就是平面朝向。

`RViz` 是 ROS2 的可视化工具。它自己不产生导航、不产生传感器数据，也不替机器人做决策。它订阅 topic，查询 tf，然后把机器人状态、坐标轴、雷达点、图像、路径、地图和 costmap 画出来。今天 RViz 左侧最重要的是 `Global Options -> Fixed Frame` 和各个 display 的状态；中间主视图区看 TF 坐标轴和 LaserScan；左下角 Image 面板看图像流；右侧 Views 只是调整观察视角，不影响 ROS2 系统本身。

## 常用观察命令

`ros2 topic list` 用来查看当前系统有哪些 topic。它回答的是“系统里有哪些数据通道存在”，例如 `/tf`、`/tf_static`、`/scan`、`/image`。

`ros2 topic echo /tf_static` 用来查看静态 tf 原始消息。重点看 `header.frame_id`、`child_frame_id`、`translation` 和 `rotation`。其中父 frame 和子 frame 决定坐标树结构，平移和旋转决定子坐标系相对父坐标系的位置和朝向。

`ros2 run tf2_ros tf2_echo map base_link` 用来查询 `base_link` 相对于 `map` 的位置和姿态。它不是只看直接边，而是会沿着 tf tree 自动串联 `map -> odom -> base_link`。这条命令在 Nav2 中非常关键，因为导航首先要知道机器人身体在地图里的位置。

`ros2 run tf2_ros tf2_echo base_link laser_frame` 用来查询雷达相对于机器人本体的位置。如果实际 LaserScan 消息里的 `frame_id` 是 `single_rrbot_hokuyo_link`，则应改查 `base_link single_rrbot_hokuyo_link`。这类命令用于确认传感器是否正确挂在机器人身体上。

`ros2 run tf2_ros tf2_monitor map base_link` 用来监控 `map` 到 `base_link` 这条变换链的频率、延迟和时间戳状态。真实机器人里，很多 tf 问题不是 frame 完全不存在，而是 transform 发布太慢、时间戳过期或延迟太大。

`ros2 run tf2_tools view_frames` 用来导出当前 tf tree。今天生成的 `frames_2026-06-21_21.27.25.pdf` 就是这个命令的产物。它适合快速判断 frame 是否存在、父子关系是否连通、有没有孤立的坐标树。

## 项目连接

在风机巡检小项目中，tf2 决定了机器人能不能把导航、传感器和地图对到同一个空间里。比如相机拍到风机目标时，图像本身只是 `/image` topic 上的一帧数据；要知道这帧图像是机器人从哪个位置、哪个朝向采集的，就必须结合 `camera_frame -> base_link -> odom -> map`。

同理，雷达 `/scan` 的每个距离点默认只在雷达坐标系里有意义。Nav2 要把障碍物放进 costmap，就必须知道 `map -> odom -> base_link -> laser_frame` 或 `map -> odom -> base_link -> single_rrbot_hokuyo_link` 这条链。如果这条链断了，雷达数据即使存在，也不能正确用于可视化或避障。

今天的练习看起来只是几条静态 transform，但它提前建立了 Day 6-9 的调试方法。后面进入 Gazebo、TurtleBot 和 Nav2 时，遇到机器人不显示、雷达不显示、costmap 不更新、Nav2 报 frame 错误，都应该先按“topic 是否存在 -> 消息 frame_id 是什么 -> tf tree 是否连通 -> 时间戳是否正常”的顺序排查。

## 踩坑记录

<span style="color:red">用户提问：RViz 里 Image 和 LaserScan 显示 `Error subscribing: Empty topic name` 是什么原因？</span>

原因是 RViz display 的 `Topic` 字段还没有选具体话题。解决方式是在 `Image` 中选择 `/image`，在 `LaserScan` 中选择 `/scan`。这个错误和 tf tree 无关，属于 display 没有订阅目标。

<span style="color:red">用户提问：`frames_2026-06-21_21.27.25.pdf` 和 RViz 里这些终端分别起什么作用？</span>

理解方式是：`static_transform_publisher` 发布坐标系之间的父子关系，`dummy_laser` 发布模拟雷达数据，`cam2image` 发布模拟图像数据，`view_frames` 导出坐标树，`rviz2` 把 topic 和 tf 组合起来画出来。PDF 是坐标树证据，RViz 是实时可视化窗口。

<span style="color:red">用户提问：图里几个坐标系分别指什么？</span>

右侧重合的坐标系通常对应 `map/odom`，因为今天发布的 `map -> odom` 是零位移、零旋转；中间是 `base_link`，表示机器人身体中心；左侧两个是相机和雷达传感器坐标系，表示传感器安装在机器人身体上的位置。

<span style="color:red">用户提问：`static_transform_publisher --x 1.0 --y 0.5 --z 0 --yaw 0.3 --frame-id odom --child-frame-id base_link` 该怎么理解？</span>

这条命令表示在 `odom` 坐标系中，`base_link` 位于 `(1.0, 0.5, 0)`，并且绕 Z 轴旋转 `0.3` 弧度。`frame-id` 是父坐标系，`child-frame-id` 是子坐标系，`x/y/z` 是平移，`roll/pitch/yaw` 是旋转。

<span style="color:red">用户提问：`ros2 topic list`、`ros2 topic echo /tf_static`、`tf2_echo`、`tf2_monitor` 分别观察什么？</span>

`ros2 topic list` 看当前有哪些数据通道；`ros2 topic echo /tf_static` 看静态坐标关系的原始消息；`tf2_echo map base_link` 查机器人身体在地图里的位置；`tf2_echo base_link laser_frame` 查传感器安装位置；`tf2_monitor map base_link` 查这条坐标链是否稳定、及时。

## 八股自测

Q：tf2 在 ROS2 机器人开发里解决什么问题？
A：tf2 解决不同坐标系之间的位置和朝向关系。机器人身体、地图、相机、雷达都有自己的 frame，tf2 让系统能查询任意两个 frame 在某个时间点的相对变换。

Q：`map`、`odom`、`base_link`、`sensor frame` 分别是什么？
A：`map` 是全局地图坐标，`odom` 是连续但可能漂移的里程计坐标，`base_link` 是机器人本体坐标，`sensor frame` 是相机或雷达自己的坐标。典型链路是 `map -> odom -> base_link -> sensor`。

Q：为什么有了 `/scan` 还必须有 tf？
A：`/scan` 只提供雷达测到的距离数据，并说明这些数据属于哪个 `frame_id`。RViz 或 Nav2 要把这些点放进地图，就必须通过 tf 查到从 `map` 到该雷达 frame 的变换。

Q：RViz 的 Fixed Frame 为什么重要？
A：Fixed Frame 是 RViz 用来统一显示所有数据的参考坐标系。若设置为 `map`，RViz 会尝试把 TF、LaserScan、Image、路径和机器人模型都转换到 `map` 下显示；如果 tf tree 连不到 `map`，对应 display 就会报错。

Q：`static_transform_publisher` 适合发布什么？
A：适合发布固定不变的坐标关系，比如 `base_link -> camera_frame` 或 `base_link -> laser_frame`。真实机器人中 `odom -> base_link` 会随机器人运动变化，通常应由里程计或仿真器动态发布，今天只是为了教学临时静态化。

Q：排查 RViz 显示异常的顺序是什么？
A：先用 `ros2 topic list -t` 确认 topic 存在，再用 `ros2 topic echo --once` 看消息和 `frame_id`，然后用 `view_frames` 或 `tf2_echo` 检查从 Fixed Frame 到该 `frame_id` 是否连通，最后再看时间戳和发布频率。

## 明日衔接

明天进入 Day 6：Gazebo 仿真与 TurtleBot。今天的坐标树是手动搭出来的，明天会在仿真机器人中观察这些关系如何由 Gazebo、robot_state_publisher、里程计和传感器节点自动发布，并进一步观察 `/cmd_vel`、`/odom`、`/scan` 和相机话题。

# 2026-06-22 Day 6：Gazebo 仿真、TurtleBot 与 rosbag

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 6：Gazebo 仿真与 TurtleBot。Day 5 手动搭了一个教学用 tf tree，今天进入真正的仿真机器人系统：Gazebo 负责生成虚拟世界、机器人运动和传感器数据，ROS2 负责用 node、topic、tf 和 rosbag 把这些数据组织起来。

Day 6 在风机巡检小项目里的作用是建立低风险试验场。后续不可能一开始就拿真实机器人围着真实风机跑，所以要先在 Gazebo 中验证机器人能动、雷达有数据、里程计有数据、tf 能连通、rosbag 能回放。这些能力是 Day 7 Nav2 自主导航和 Day 14 数据采集复盘的基础。

## 今日完成任务

今天启动了 TurtleBot3 Gazebo 仿真，并通过 `teleop_keyboard` 遥控机器人。系统中观察到 `/robot_state_publisher`、`/ros_gz_bridge` 和 `/teleop_keyboard` 三个核心节点。`/cmd_vel` 由键盘遥控节点发布、由 `ros_gz_bridge` 订阅，说明控制命令能从 ROS2 进入 Gazebo。`/odom` 和 `/scan` 由 `ros_gz_bridge` 发布，说明 Gazebo 中的仿真运动和虚拟雷达数据能进入 ROS2。

今天还排查了 Gazebo 启动中的环境问题：Jazzy 使用 Gazebo Sim 8，`gz` 可执行文件和命令配置位于 ROS vendor 目录下。若当前 shell 没有正确设置 `PATH` 和 `GZ_CONFIG_PATH`，`turtlebot3_gazebo` launch 可能报 `'NoneType' object has no attribute 'lower'`，本质原因是 Gazebo 命令入口没有被正确找到。

今天录制了一个 rosbag，路径为 `/tmp/ros2_day6_bag/rosbag2_2026_06_22-21_27_14`。它记录了 81.6 秒、9628 条消息，包括 `/cmd_vel`、`/odom`、`/scan`、`/tf` 和 `/tf_static`。这说明 Day 6 已经不只是“看见仿真界面”，而是把机器人运动和传感器数据保存成了可回放实验材料。

今天最重要的收获是：**Gazebo 负责产生仿真世界和传感器数据，ROS2 topic 负责传输这些数据，RViz 负责订阅并可视化，rosbag 负责把 topic 数据录下来以后复盘。**

## 基本概念

`Gazebo` 是机器人开发中的仿真试验场。它模拟地面、障碍物、机器人模型、传感器、碰撞和运动。真实机器人调试成本高，也容易受场地、硬件和安全限制影响；Gazebo 让开发者可以先在虚拟环境里验证控制、感知、导航和数据采集链路。

`ros_gz_bridge` 是 Gazebo 和 ROS2 之间的桥。Gazebo 内部有自己的仿真通信系统，ROS2 有自己的 topic、message 和 node。bridge 的作用是把 Gazebo 中的激光雷达、里程计、时钟等数据转换成 ROS2 topic，也把 ROS2 里的 `/cmd_vel` 控制命令送回 Gazebo。

`/cmd_vel` 是速度命令 topic。今天它的类型是 `geometry_msgs/msg/TwistStamped`，发布者是 `teleop_keyboard`，订阅者是 `ros_gz_bridge`。这条链路说明键盘按键会变成速度命令，再通过 bridge 驱动 Gazebo 中的 TurtleBot。

`/odom` 是里程计 topic。它的类型是 `nav_msgs/msg/Odometry`，消息中 `frame_id: odom`、`child_frame_id: base_footprint` 表示这条消息描述的是机器人底盘在 `odom` 坐标系中的位姿和速度。后续 Nav2 需要持续知道机器人在哪里，`/odom` 就是关键状态来源之一。

`/scan` 是激光雷达 topic。它的类型是 `sensor_msgs/msg/LaserScan`，消息中 `frame_id: base_scan` 表示数据来自雷达坐标系。`ranges` 是一圈扫描中的距离数组，`.inf` 表示该方向在最大探测距离内没有打到障碍物，具体数字如 `0.92` 表示该方向约 0.92 米处有障碍物。

`/tf` 和 `/tf_static` 是坐标变换 topic。`/tf_static` 适合保存固定安装关系，例如雷达相对于车体的位置；`/tf` 适合保存动态关系，例如机器人随时间变化的 `odom -> base_footprint`。RViz 和 Nav2 都需要依赖这些变换把雷达点、机器人模型、路径和地图放进同一个空间里。

`rosbag` 是 ROS2 的数据录像，不是屏幕视频。它录下的是 topic 消息本身。今天的 bag 中 `/odom` 有 3505 条，说明里程计持续更新；`/scan` 有 350 条，说明雷达数据被记录；`/tf` 有 4936 条，说明坐标变换也被保存。`ros2 bag play` 会把这些消息按原时间顺序重新发布出来，供 RViz、命令行或分析脚本订阅。

## 常用观察命令

`ros2 node list` 用来确认当前有哪些模块活着。今天看到的 `/robot_state_publisher`、`/ros_gz_bridge`、`/teleop_keyboard` 分别对应机器人模型与坐标发布、Gazebo/ROS2 桥接、键盘控制。

`ros2 topic list -t` 用来确认系统里有哪些数据通道，以及每个 topic 的消息类型。只看名字不够，还要看类型，因为不同工具或节点只有在消息类型匹配时才能正确通信。

`ros2 topic info -v /cmd_vel` 用来确认某个 topic 的发布者和订阅者。今天它证明了 `teleop_keyboard -> /cmd_vel -> ros_gz_bridge` 这条控制链路是通的。

`ros2 topic echo /odom --once` 和 `ros2 topic echo /scan --once` 用来抽样看一条真实消息。`--once` 很适合学习和排查，因为它不会持续刷屏，只看一帧就能知道 frame、字段和数据是否合理。

`ros2 topic hz /odom`、`ros2 topic hz /scan` 用来查看话题频率。机器人系统不是只要有一条消息就行，而是需要持续、稳定、够快的数据流。`/scan` 太慢会导致障碍物更新滞后，`/odom` 不稳定会影响定位和控制，`/tf` 延迟过大可能让 RViz 或 Nav2 报 transform 错误。

`ros2 bag info <bag_dir>` 用来检查 bag 里录了哪些 topic、每个 topic 有多少条消息、总时长和存储格式。`ros2 bag play <bag_dir>` 用来重放这些 topic，但它不会自动显示画面，必须有 RViz 或其他订阅者去接收并可视化这些消息。

## 项目连接

在风机巡检小项目里，今天的 TurtleBot 仿真就是后续 `blade_inspection_orbit_demo` 的低成本原型。当前是键盘遥控机器人，Day 7 之后会变成 Nav2 自主发目标；当前观察的是 `/scan` 和 `/odom`，Day 13-14 会增加相机图像、位姿日志和任务 CSV；当前录的是基础 bag，后续会录制能支撑回放、排查和离线分析的完整实验数据。

看节点、话题和频率的意义在后续会越来越明显。Nav2 导航失败时，要先确认 planner、controller、map server、AMCL 等节点是否存在；机器人不动时，要查 `/cmd_vel` 是否有 publisher 和 subscriber；雷达避障不工作时，要查 `/scan` 是否存在、frame 是否能接入 tf tree、频率是否稳定；RViz 空白时，要查 Fixed Frame、`/robot_description`、`/tf` 和显示项订阅的 topic。

今天也提前理解了 rosbag 的价值。风机巡检任务中，机器人每个航点拍到的图像、当时的位姿、雷达状态和 tf 都需要能复盘。rosbag 让实验从“一次性现场现象”变成“可以回放、可以分析、可以给别人检查的数据材料”。

## 踩坑记录

<span style="color:red">用户遇到：`ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py` 报 `'NoneType' object has no attribute 'lower'`。</span>

排查结果是当前 Jazzy 的 Gazebo Sim vendor 环境没有完整暴露到 shell 中。`gz` 位于 `/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz`，同时还需要 `GZ_CONFIG_PATH` 指向各 vendor 包的 `share/gz` 目录。补充这些环境变量后，`gz sim --versions` 能输出 `8.11.0`，说明 Gazebo Sim 命令入口可用。

<span style="color:red">用户提问：Gazebo 在机器人开发中起到什么作用？</span>

Gazebo 是仿真试验场，负责让虚拟机器人在虚拟世界里运动，并生成虚拟雷达、相机、里程计等数据。它降低了真实机器人调试成本，让导航、避障、采集和数据回放可以先在仿真中跑通。

<span style="color:red">用户提问：查看节点、话题和某个话题频率的实际意义在哪里？</span>

节点说明模块是否启动，话题说明数据通道是否存在，发布者/订阅者说明模块之间是否接上，频率说明数据是否持续稳定。后续调试 Nav2、SLAM、RViz 和数据采集时，通常都要按“node 是否存在 -> topic 是否存在 -> pub/sub 是否接上 -> echo 内容是否合理 -> hz 是否稳定”的顺序排查。

<span style="color:red">用户提问：RViz 里什么都没有，应该怎么看到仿真机器人？</span>

Day 6 阶段应先把 `Fixed Frame` 设为 `odom`，再添加 `TF`、`RobotModel` 和 `/scan` 对应的 `LaserScan` display。`RobotModel` 需要订阅 `/robot_description`；`LaserScan` 需要订阅 `/scan`；两者都需要 tf 能把相关 frame 转换到 `odom` 下。

<span style="color:red">用户提问：rosbag 是什么，点击 play 后显示在哪里？</span>

rosbag 是 topic 数据录像，不是视频文件。`ros2 bag play` 只是重新发布录下来的 topic，不会自动弹出画面。想看到效果，需要同时打开 RViz 并订阅 `/scan`、`/tf`、`/odom` 等数据；想看完整机器人模型，还需要有 `/robot_description`。

## 八股自测

Q：Gazebo 和 RViz 的区别是什么？
A：Gazebo 是仿真器，负责模拟世界、机器人运动、传感器和碰撞；RViz 是可视化工具，负责订阅 ROS2 topic 和查询 tf 后把数据画出来。Gazebo 产生数据，RViz 展示数据。

Q：`ros_gz_bridge` 为什么重要？
A：Gazebo 和 ROS2 的通信系统不同。`ros_gz_bridge` 把 Gazebo 中的仿真数据转换成 ROS2 topic，也把 ROS2 的控制命令送进 Gazebo，是仿真和 ROS2 节点协作的桥。

Q：为什么机器人不动时要查 `/cmd_vel`？
A：`/cmd_vel` 是速度命令。如果没有 publisher，说明没有控制源；如果没有 subscriber，说明命令没人执行；如果类型不匹配或频率异常，Gazebo 或底盘控制器也可能无法正确接收。

Q：为什么有 `/scan` 还要看频率？
A：雷达数据需要持续更新。只有一条 `/scan` 消息不能支撑避障和 costmap 更新；频率太低会导致障碍物信息滞后，导航表现会变差。

Q：`ros2 bag play` 后为什么没有画面？
A：因为 bag play 只是重新发布 topic。画面需要 RViz、图像工具或其他订阅者来显示。没有订阅者时，消息仍然在发布，但用户不会直接看到可视化效果。

Q：今天录的 bag 为什么没法单独显示完整 RobotModel？
A：因为 bag 录了 `/cmd_vel`、`/odom`、`/scan`、`/tf`、`/tf_static`，但没有录 `/robot_description`。RViz 的 RobotModel 需要机器人模型描述，所以单独回放 bag 时可能只能显示 TF 和 LaserScan。

## 明日衔接

明天进入 Day 7：Nav2 第一次导航。今天已经确认仿真机器人能启动、能被键盘控制、能发布里程计和雷达数据，并且能录制 rosbag。下一步是在同一仿真基础上启动 Nav2，让机器人从手动遥控进入 RViz 目标点自主导航。

# 2026-06-23 Day 7：Nav2 第一次导航

## 今日学习位置

今天对应 `DOCS/PLAN.md` 的 Stage 2：仿真与导航基础，以及 Day 7：Nav2 第一次导航。Day 6 已经验证 Gazebo 中的 TurtleBot 能手动遥控、能发布 `/odom`、`/scan` 和 `/tf`；今天在同一仿真基础上启动 Nav2，让机器人从“人按键盘控制”进入“给一个目标点后自主导航”。

Day 7 在风机巡检小项目里的作用很直接：后续机器人围绕风机目标移动，不应该靠人工遥控，而应该靠 Nav2 接收一组巡检航点，自动规划路径并输出速度命令。今天先用 RViz 手动点目标，是为了把 Nav2 的基础链路跑通。

## 今日完成任务

今天启动了 `nav2_bringup` 的 TurtleBot3 仿真导航示例，使用 RViz 观察地图、costmap、AMCL 粒子云、全局路径和局部控制状态。最开始 RViz 中 `Startup` 按钮灰色不可点，终端反复提示 `Frame does not exist`。排查后确认这不是 RViz 按钮本身的问题，而是 Nav2 lifecycle 已经自动激活，AMCL 还没有收到初始位姿，因此 `map -> odom` 没有建立。

随后使用 `2D Pose Estimate` 在地图中给 AMCL 设置机器人初始位姿，让 localization 进入 active。通过 `tf2_echo odom base_footprint` 和 `tf2_echo map odom` 明确区分了两条链路：`odom -> base_footprint` 说明 Gazebo/里程计知道机器人相对起点的位置，`map -> odom` 说明 AMCL 知道机器人在全局地图里的位置。

今天还排查了 RViz `RobotModel` 的 URDF/mesh 加载错误。报错不是 tf 或 Nav2 算法问题，而是 `nav2_minimal_tb3_sim` 的 URDF 引用 `package://nav2_minimal_tb3_sim/models/*.dae`，但实际 mesh 文件位于 `models/turtlebot3_model/meshes/`。修复资源路径后，RobotModel 能正常显示。

今天最重要的收获是：**Nav2 负责把“目标点”变成“可执行的速度命令”，RViz 负责发目标和看状态，Gazebo 负责模拟世界和机器人运动。**

## 基本概念

`AMCL` 全名是 Adaptive Monte Carlo Localization，可以先理解成“用地图、雷达和里程计估计机器人在地图哪里”的定位模块。它会维护一堆可能位置，也就是粒子；当雷达扫描和地图障碍物越匹配，粒子就越集中，机器人在地图中的位置估计就越可信。Nav2 需要 AMCL 发布 `map -> odom`，否则系统只有里程计坐标，不知道机器人在全局地图中的位置。

`2D Pose Estimate` 是给 AMCL 的初始位姿提示。它不会移动 Gazebo 里的机器人，也不是直接控制机器人，而是在告诉定位模块：“机器人现在大概在地图这个位置，朝这个方向。”箭头起点是初始位置，箭头方向是机器人朝向。设置以后，AMCL 才能从这个附近开始用雷达和地图匹配。

`Nav2 Goal` 是给 Nav2 的导航目标。它和 `2D Pose Estimate` 不同：`2D Pose Estimate` 是告诉系统“我现在在哪里”，`Nav2 Goal` 是告诉系统“我要去哪里”。前者服务定位，后者触发导航。

`planner` 负责从当前位姿到目标位姿规划全局路径。它考虑地图、障碍物和代价地图，输出一条大方向上的路线。

`controller` 负责把规划路径变成实时速度命令。机器人不会一次性“跳到路径上”，而是控制器不断根据当前位置和路径误差发布 `/cmd_vel`，让机器人逐步跟踪路径。

`costmap` 是导航用的代价地图。白色可通行区域、黑色障碍物、粉色或青色膨胀区域，都在告诉 Nav2 哪些地方安全、哪些地方危险、哪些地方不能作为目标点。目标点如果放在墙、柱子或膨胀区里，导航可能失败或绕路异常。

`/cmd_vel` 是 Nav2 给底盘的速度意图。仿真里它被 Gazebo bridge 转成仿真机器人运动；真实机器人里它会被底盘驱动或控制器转成电机、轮子或转向执行。Nav2 不直接控制电机，它输出的是导航层面的速度命令。

## 常用观察命令

`ros2 run tf2_ros tf2_echo odom base_footprint` 用来确认 Gazebo/里程计到机器人底盘的变换是否存在。如果这条有输出，说明仿真机器人自身位姿链路是活的。

`ros2 run tf2_ros tf2_echo map odom` 用来确认 AMCL 是否已经建立全局地图到里程计坐标的关系。如果这条一直提示 `map` frame 不存在，通常说明 AMCL 还没有初始化或 localization 没有 active。

`ros2 topic echo /amcl_pose --once` 用来查看 AMCL 当前估计的机器人位姿。它适合验证 `2D Pose Estimate` 后定位是否真正有输出。

`ros2 topic echo /cmd_vel --once` 用来确认 Nav2 是否正在给机器人发速度命令。发出 `Nav2 Goal` 后如果 `/cmd_vel` 有非零输出，说明 controller 已经开始控制机器人。

`ros2 action info /navigate_to_pose` 用来查看 Nav2 导航 action 的连接情况。RViz 点击 `Nav2 Goal`，本质上就是向这个导航 action 发送目标。

## 项目连接

在风机巡检小项目中，Nav2 后续会承担“到达巡检观测点”的核心职责。Day 10 之后，我们不会一直用 RViz 手点目标，而会用 Python 脚本或 `BasicNavigator` 自动发目标点；Day 11-12 会把单个目标扩展成多航点和环绕目标航点；Day 13-14 会在每个航点采集图像、记录位姿并录制 rosbag。

因此，今天的 RViz 手动导航不是最终形态，而是确认 Nav2 基础能力可用：系统能定位机器人，能生成路径，能避开障碍物，能发布速度命令，Gazebo 中的机器人能跟着执行。只要这条链路稳定，后续把“手点目标”替换成“脚本自动发航点”就有了基础。

真实机器人开发中，Nav2 也不是单个算法，而是一套导航框架。它把定位、路径规划、局部控制、障碍物代价地图、任务行为树和恢复行为组织在一起。传感器和底盘驱动提供 `/scan`、`/odom`、`/tf`，Nav2 根据这些输入输出 `/cmd_vel`，底盘控制器再把 `/cmd_vel` 变成实际电机运动。

## 踩坑记录

<span style="color:red">用户遇到：RViz 左下角 `Startup` 是灰色，无法点击。</span>

判断结果是当前 `nav2_bringup` 示例已经由 lifecycle manager 自动激活，不需要手动点 `Startup`。真正需要处理的是 AMCL 初始位姿和 `map -> odom` 变换链路。

<span style="color:red">用户遇到：终端一直显示 `Frame does not exist`。</span>

一开始 `map -> odom` 不存在，是因为 AMCL 还没有收到初始位姿。`2D Pose Estimate` 之后，AMCL 才能发布 `map -> odom`，RViz 中以 `map` 为 Fixed Frame 的显示项才能正常工作。

<span style="color:red">用户提问：AMCL 是什么？</span>

AMCL 是定位模块，用地图、雷达和里程计估计机器人在地图中的位置。它不是负责规划路径的模块，而是给 Nav2 提供“机器人现在在哪里”的基础信息。

<span style="color:red">用户提问：`2D Pose Estimate` 到底是在干什么？怎么判断应该点哪里？</span>

`2D Pose Estimate` 是给 AMCL 一个初始猜测。刚启动且机器人未移动时，通常可以先放在地图中心或 Gazebo 起点附近；如果 RViz 在 `map` 下看不到机器人，可以先把 Fixed Frame 改为 `odom`，通过 RobotModel、TF 或 `/odom` 判断机器人相对起点的位置，再回到 `map` 下设置初始位姿。

<span style="color:red">用户遇到：RViz `RobotModel` 报 URDF/mesh 加载错误。</span>

排查结果是 `nav2_minimal_tb3_sim` 的 URDF 引用路径和实际 mesh 文件位置不一致。RViz 在找 `package://nav2_minimal_tb3_sim/models/waffle_base.dae` 等文件，而实际文件在 `models/turtlebot3_model/meshes/` 下。这会影响机器人外壳显示，但不等同于 Nav2 定位或规划失败。

<span style="color:red">用户提问：真实机器人开发中 Nav2 主要负责什么？它是导航算法吗？</span>

Nav2 更准确地说是一套导航框架，不是单个算法。它内部包含 AMCL、planner、controller、costmap、behavior tree navigator 等模块，负责把“目标点”转成“可执行的 `/cmd_vel` 速度命令”。真实底盘驱动再把 `/cmd_vel` 转成电机和轮子运动。

## 八股自测

Q：Nav2 在机器人系统中负责哪一层？
A：Nav2 负责导航决策层，把目标点、地图、定位、障碍物和机器人状态综合起来，规划路径并输出 `/cmd_vel`。它不直接控制电机，底盘驱动负责执行速度命令。

Q：RViz、Gazebo、Nav2 三者有什么区别？
A：RViz 是可视化和交互工具，Gazebo 是仿真器，Nav2 是导航系统。RViz 发目标和看状态，Gazebo 模拟机器人和传感器，Nav2 做定位、规划、控制并发布速度命令。

Q：`2D Pose Estimate` 和 `Nav2 Goal` 有什么区别？
A：`2D Pose Estimate` 告诉 AMCL “机器人现在大概在哪里”；`Nav2 Goal` 告诉 Nav2 “机器人要去哪里”。前者解决定位初始化，后者触发导航任务。

Q：为什么 `map -> odom` 对 Nav2 很重要？
A：`odom -> base_footprint` 只能说明机器人相对启动点怎么动，`map -> odom` 才能把机器人放进全局地图。没有 `map -> odom`，Nav2 就无法可靠判断机器人在地图里的位置。

Q：为什么目标点不能随便点在障碍物附近？
A：Nav2 会根据 costmap 判断可通行区域。黑色墙体、柱子和膨胀区代表障碍物或安全距离，目标点放在那里可能不可达，planner 或 controller 会失败。

Q：真实机器人中 Nav2 的输入和输出分别是什么？
A：输入主要是地图、目标点、`/scan`、`/odom`、`/tf` 和参数；输出主要是 `/cmd_vel`。底盘控制器再把 `/cmd_vel` 转成真实运动。

## 明日衔接

明天进入 Day 8：Nav2 架构与低风险参数调试。今天已经从 RViz 目标点跑通导航链路，明天要开始把 Nav2 从“能用的黑盒”拆成 planner、controller、costmap、goal checker 等模块，并尝试修改少量低风险参数，观察速度、安全距离和到点容差如何影响机器人行为。
