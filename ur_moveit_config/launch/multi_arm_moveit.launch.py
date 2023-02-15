from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition

def launch_setup(context, *args, **kwargs):
    use_sim_time = LaunchConfiguration("use_sim_time")
    launch_robot_1 = LaunchConfiguration("robot_1")
    launch_robot_2 = LaunchConfiguration("robot_2")


    robot_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ur_moveit_config"), "/launch", "/ur_moveit.launch.py"]
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "ur_type": "ur10e",
            "ns": "robot_1",
            "prefix": "robot_1_",
            "rviz_config_file": "robot_1.rviz",
            "pose_xyz": '"0 -0.5 0"',
            "pose_rpy": '"0 0 -1.5707963"',
        }.items(),
        condition=IfCondition(launch_robot_1),
    )
    robot_2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ur_moveit_config"), "/launch", "/ur_moveit.launch.py"]
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "ur_type": "ur10e",
            "ns": "robot_2",
            "prefix": "robot_2_",
            "rviz_config_file": "robot_2.rviz",
            "pose_xyz": '"0 0.5 0"',
            "pose_rpy": '"0 0 1.5707963"',
        }.items(),
        condition=IfCondition(launch_robot_2),
    )

    nodes_to_start = [
        robot_1,
        robot_2,
    ]

    return nodes_to_start

def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_1",
            default_value="false",
            description="Launch robot 1 or not",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_2",
            default_value="false",
            description="Launch robot 2 or not",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Using sim time or not",
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])