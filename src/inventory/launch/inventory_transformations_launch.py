import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([ 
        Node(
            package='inventory',  # Replace with your Inventory package name
            executable='inventory_transformations',     # Replace with your Inventory manager node name
            name='inventory_transformations',
            output='screen'
        ),

    ])