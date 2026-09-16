#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class BrainTransformationsNode(Node):
    def __init__(self):
        super().__init__('brain_transformations_node')

        # Initialize the static transform broadcaster
        self.broadcaster = StaticTransformBroadcaster(self)

        # Define and send transformations
        self.send_transformations()

    def send_transformations(self):
        # Create a list to hold transforms
        transforms = []

        # Transform from map to base_link
        t1 = TransformStamped()
        t1.header.stamp = self.get_clock().now().to_msg()
        t1.header.frame_id = 'map'
        t1.child_frame_id = 'base_link'
        t1.transform.translation.x = 1.0
        t1.transform.translation.y = 1.0
        t1.transform.translation.z = 0.0
        t1.transform.rotation.x = 0.0
        t1.transform.rotation.y = 0.0
        t1.transform.rotation.z = 0.0
        t1.transform.rotation.w = 1.0
        transforms.append(t1)

        # Transform from base_link to arm_link
        t2 = TransformStamped()
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = 'base_link'
        t2.child_frame_id = 'arm_link'
        t2.transform.translation.x = 0.1
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.2
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0
        transforms.append(t2)

        # Transform from arm_link to camera_link
        t3 = TransformStamped()
        t3.header.stamp = self.get_clock().now().to_msg()
        t3.header.frame_id = 'base_link'
        t3.child_frame_id = 'camera_link'
        t3.transform.translation.x = -0.5
        t3.transform.translation.y = 0.0
        t3.transform.translation.z = 0.5
        t3.transform.rotation.x = 0.0
        t3.transform.rotation.y = math.sin(math.pi / 12)  # Example rotation
        t3.transform.rotation.z = 0.0
        t3.transform.rotation.w = math.cos(math.pi / 12)  # Example rotation
        transforms.append(t3)

        # Broadcast the transforms
        self.broadcaster.sendTransform(transforms)
        self.get_logger().info('Published static transforms for map, base_link, arm_link, and camera_link.')

def main(args=None):
    rclpy.init(args=args)
    node = BrainTransformationsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
