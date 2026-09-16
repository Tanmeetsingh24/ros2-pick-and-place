#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class InventoryTransformations(Node):
    def __init__(self):
        super().__init__('inventory_transformations')

        # Initialize the static broadcaster
        self.broadcaster = StaticTransformBroadcaster(self)

        # Define and send transformations
        self.send_transformations()

    def send_transformations(self):
        # Define the three inventory slots relative to the base link
        transforms = []

        # Inventory Slot 1
        t1 = TransformStamped()
        t1.header.stamp = self.get_clock().now().to_msg()
        t1.header.frame_id = 'base_link'
        t1.child_frame_id = 'inventory_slot_1'
        t1.transform.translation.x = 0.25
        t1.transform.translation.y = 0.25
        t1.transform.translation.z = 0.0
        t1.transform.rotation.x = 0.0
        t1.transform.rotation.y = 0.0
        t1.transform.rotation.z = math.sin(math.pi / 8)
        t1.transform.rotation.w = math.cos(math.pi / 8)
        transforms.append(t1)

        # Inventory Slot 2
        t2 = TransformStamped()
        t2.header.stamp = self.get_clock().now().to_msg()
        t2.header.frame_id = 'base_link'
        t2.child_frame_id = 'inventory_slot_2'
        t2.transform.translation.x = 0.25
        t2.transform.translation.y = 0.0
        t2.transform.translation.z = 0.0
        t2.transform.rotation.x = 0.0
        t2.transform.rotation.y = 0.0
        t2.transform.rotation.z = 0.0
        t2.transform.rotation.w = 1.0
        transforms.append(t2)

        # Inventory Slot 3
        t3 = TransformStamped()
        t3.header.stamp = self.get_clock().now().to_msg()
        t3.header.frame_id = 'base_link'
        t3.child_frame_id = 'inventory_slot_3'
        t3.transform.translation.x = 0.25
        t3.transform.translation.y = -0.25
        t3.transform.translation.z = 0.0
        t3.transform.rotation.x = 0.0
        t3.transform.rotation.y = 0.0
        t3.transform.rotation.z = math.sin(-math.pi / 8)
        t3.transform.rotation.w = math.cos(-math.pi / 8)
        transforms.append(t3)

        # Broadcast the transforms
        self.broadcaster.sendTransform(transforms)
        self.get_logger().info('Published static transforms for inventory slots.')

def main(args=None):
    rclpy.init(args=args)
    node = InventoryTransformations()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
