import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='inventory',
            executable='inventory_transformations',
            name='inventory_manager',
            output='screen'
        ),
    ])
