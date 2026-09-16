import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Int32MultiArray
from interfaces.msg import Camera


class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscription to the Camera topic
        self.camera_subscriber = self.create_subscription(
            Camera,
            'camera',
            self.camera_callback,
            10
        )

        # Publisher for perception status
        self.perception_status_pub = self.create_publisher(Int32MultiArray, 'perception_status', 10)

        # Store seen item IDs (unique and limited to the last 5)
        self.seen_item_ids = set()  # Use a set to store unique item IDs
        self.item_id_history = []   # List to keep a history of the last 5 unique item IDs

        # Timer to clear and publish perception status every second
        self.timer = self.create_timer(1.0, self.publish_perception_status)

    def camera_callback(self, msg):
        # Broadcast the transformation for the detected item
        self.broadcast_item_transform(msg)
        
        # If the item is not already seen, add it to the set and the history list
        if msg.item_id not in self.seen_item_ids:
            self.seen_item_ids.add(msg.item_id)
            self.item_id_history.append(msg.item_id)

            # Keep the history limited to the last 5 unique items
            if len(self.item_id_history) > 5:
                # Remove the oldest item from both the set and the list
                oldest_item = self.item_id_history.pop(0)
                self.seen_item_ids.remove(oldest_item)

        self.get_logger().info(f'Item {msg.item_id} detected and added to perception history')

    def broadcast_item_transform(self, msg):
        # Create and broadcast a transform from the camera link to the item
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'camera_link'  # Parent frame
        t.child_frame_id = f'item_{msg.item_id}'  # Unique frame for each item
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = msg.z
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0  # No rotation

        # Broadcast the transform
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info(f'Published transform for item {msg.item_id}')

    def publish_perception_status(self):
        # Publish the list of seen item IDs
        msg = Int32MultiArray()
        msg.data = self.item_id_history  # Publish the history of the last 5 unique item IDs
        self.perception_status_pub.publish(msg)
        self.get_logger().info(f'Published perception status: {self.item_id_history}')


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
