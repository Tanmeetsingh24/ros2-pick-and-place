import os
from launch import LaunchDescription
from launch_ros.actions import Node
 
def generate_launch_description():
    return LaunchDescription([
        # Launch the Brain Node
        Node(
            package='brain',  # Replace with your Brain package name
            executable='brain_node',       # Replace with your Brain node name
            name='brain_node',
            output='screen'
        ),
        # Launch the Inventory Manager
        Node(
            package='inventory',  # Replace with your Inventory package name
            executable='inventory_manager',     # Replace with your Inventory manager node name
            name='inventory_manager',
            output='screen'
        ),
        
        Node(
            package='inventory',  # Replace with your Inventory package name
            executable='inventory_transformations',     # Replace with your Inventory manager node name
            name='inventory_transformations',
            output='screen'
        ),
        # Launch the Arm Movement Service
        Node(
            package='arm',  # Replace with your Arm package name
            executable='arm',    # Replace with your Arm service node name
            name='arm',
            output='screen'
        ),
        # Launch the Brain Transformations Node
        Node(
            package='brain',  # Replace with your Transformations package name
            executable='brain_transformations',  # Replace with your Transformations node name
            name='brain_transformations',
            output='screen'
        ),
        Node(
            package='perception',  # Replace with your Transformations package name
            executable='perception',  # Replace with your Transformations node name
            name='perception',
            output='screen'
        ),

    ])