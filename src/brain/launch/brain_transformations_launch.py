import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Launch the Brain Node
        Node(
            package='brain',  # Replace with your Brain package name
            executable='brain_transformations',       # Replace with your Brain node name
            name='brain_transformations',
            output='screen'
        ),
])
