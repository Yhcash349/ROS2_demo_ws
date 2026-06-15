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
