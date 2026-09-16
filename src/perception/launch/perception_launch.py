import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception',  # Replace with your Perception package name
            executable='perception',  # Replace with your Perception node executable name
            name='perception',
            output='screen'
        ),
    ])
