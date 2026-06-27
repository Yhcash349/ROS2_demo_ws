#!/usr/bin/env python3
"""Day10: use Nav2 Simple Commander to send one NavigateToPose goal."""

import argparse
import math
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def yaw_to_quaternion(yaw):
    """把平面 yaw 角转换成 ROS 使用的四元数。"""
    half_yaw = yaw * 0.5
    return {
        'z': math.sin(half_yaw),
        'w': math.cos(half_yaw),
    }


def make_pose(clock, frame_id, x, y, yaw):
    """构造 Nav2 action 需要的 PoseStamped。"""
    pose = PoseStamped()
    pose.header.frame_id = frame_id
    pose.header.stamp = clock.now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0

    quat = yaw_to_quaternion(yaw)
    pose.pose.orientation.z = quat['z']
    pose.pose.orientation.w = quat['w']
    return pose


def duration_to_seconds(duration_msg):
    """把 ROS duration 消息转为秒，便于日志阅读。"""
    return duration_msg.sec + duration_msg.nanosec * 1e-9


def parse_args():
    parser = argparse.ArgumentParser(
        description='Send one Nav2 goal with BasicNavigator.'
    )
    parser.add_argument('--frame-id', default='map')
    parser.add_argument('--initial-x', type=float, default=0.0)
    parser.add_argument('--initial-y', type=float, default=0.0)
    parser.add_argument('--initial-yaw', type=float, default=0.0)
    parser.add_argument('--goal-x', type=float, default=1.0)
    parser.add_argument('--goal-y', type=float, default=0.0)
    parser.add_argument('--goal-yaw', type=float, default=0.0)
    parser.add_argument('--timeout-sec', type=float, default=60.0)
    parser.add_argument('--feedback-period-sec', type=float, default=1.0)
    return parser.parse_args()


def task_result_to_text(result):
    if result == TaskResult.SUCCEEDED:
        return 'succeeded'
    if result == TaskResult.CANCELED:
        return 'canceled'
    if result == TaskResult.FAILED:
        return 'failed'
    return 'unknown'


def main():
    args = parse_args()

    rclpy.init()
    navigator = BasicNavigator()

    try:
        # Day10 入口：用脚本替代 RViz 的 2D Pose Estimate 和 Nav2 Goal。
        initial_pose = make_pose(
            navigator.get_clock(),
            args.frame_id,
            args.initial_x,
            args.initial_y,
            args.initial_yaw,
        )
        navigator.info(
            'Setting initial pose: '
            f'x={args.initial_x:.2f}, y={args.initial_y:.2f}, '
            f'yaw={args.initial_yaw:.2f}'
        )
        navigator.setInitialPose(initial_pose)

        navigator.info(
            'Waiting for Nav2 to become active. If you launched with '
            'autostart:=False, activate localization and navigation lifecycle '
            'managers in another terminal.'
        )
        navigator.waitUntilNav2Active()

        goal_pose = make_pose(
            navigator.get_clock(),
            args.frame_id,
            args.goal_x,
            args.goal_y,
            args.goal_yaw,
        )

        accepted = navigator.goToPose(goal_pose)
        if not accepted:
            navigator.error('Goal was rejected by Nav2.')
            return 1

        start_time = time.monotonic()
        last_feedback_time = 0.0

        while not navigator.isTaskComplete():
            now = time.monotonic()

            if now - start_time > args.timeout_sec:
                navigator.warn(
                    f'Timeout after {args.timeout_sec:.1f}s; canceling task.'
                )
                navigator.cancelTask()
                break

            if now - last_feedback_time >= args.feedback_period_sec:
                feedback = navigator.getFeedback()
                if feedback is not None:
                    nav_time = duration_to_seconds(feedback.navigation_time)
                    eta = duration_to_seconds(
                        feedback.estimated_time_remaining
                    )
                    navigator.info(
                        'Feedback: '
                        f'distance_remaining={feedback.distance_remaining:.2f} m, '
                        f'navigation_time={nav_time:.1f} s, '
                        f'eta={eta:.1f} s, '
                        f'recoveries={feedback.number_of_recoveries}'
                    )
                last_feedback_time = now

        result = navigator.getResult()
        result_text = task_result_to_text(result)
        navigator.info(f'Navigation result: {result_text}')

        return 0 if result == TaskResult.SUCCEEDED else 2

    finally:
        navigator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
