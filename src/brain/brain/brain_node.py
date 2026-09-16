#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from interfaces.srv import Inventory, ArmMovement, Command  # Import your custom services
from interfaces.msg import BrainStatus
from std_msgs.msg import Int32MultiArray  # Import for subscribing to perception status

class BrainNode(Node):
    def __init__(self):
        super().__init__('brain_node')

        # Create a service client for the Inventory Manager
        self.inventory_client = self.create_client(Inventory, 'inventory')

        # Create a service client for the Arm Movement
        self.arm_client = self.create_client(ArmMovement, 'arm')

        # Create a service for handling commands (integrated in Brain Node)
        self.command_service = self.create_service(Command, 'command', self.handle_command_service)

        # Create a subscriber for the BrainStatus topic
        self.brain_status_sub = self.create_subscription(
            BrainStatus,
            'brain_status',
            self.brain_status_callback,
            10
        )

        # Create a subscriber for Perception Node status (perception_status)
        self.perception_sub = self.create_subscription(
            Int32MultiArray,
            'perception_status',  # The topic where perception node publishes data
            self.perception_callback,
            10
        )

        # Wait for the inventory service to become available
        while not self.inventory_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Inventory service not available, waiting...')

        # Wait for the arm control service to become available
        while not self.arm_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Arm movement service not available, waiting...')

        self.get_logger().info('Brain Node, Command Service, and Perception Subscriptions have started.')

    def brain_status_callback(self, msg):
        # Handle incoming BrainStatus messages
        self.get_logger().info(f'Received BrainStatus: {msg.status}')

        # Example logic to manage inventory and arm movement
        if msg.status == "inventory_empty":
            self.handle_empty_inventory()
        elif msg.status == "item_available":
            self.handle_item_available()

    def perception_callback(self, msg):
        # Handle perception data (Int32MultiArray from perception_status)
        self.get_logger().info(f'Received Perception Status: {msg.data}')
        
        # Example: If any slot is detected as active, send command to arm to pick it up
        if any(msg.data):  # Assuming data contains slot statuses
            self.handle_item_available()

    def handle_empty_inventory(self):
        self.get_logger().info('Inventory is empty. Sending command to arm to search for items.')

        # Example command to move the arm to a predefined search position
        arm_request = ArmMovement.Request()
        arm_request.command = 'search'
        arm_request.x = 0.0
        arm_request.y = 0.0
        arm_request.z = 1.0  # Example search height

        future = self.arm_client.call_async(arm_request)
        future.add_done_callback(self.arm_response_callback)

    def handle_item_available(self):
        self.get_logger().info('Item available in inventory or from perception. Sending command to arm to pick it up.')

        arm_request = ArmMovement.Request()
        arm_request.command = 'pick'
        
        # Set the coordinates to pick up the item using x, y, z values
        arm_request.x = 0.0  # Example X position
        arm_request.y = 0.0  # Example Y position
        arm_request.z = 0.5  # Example Z position

        future = self.arm_client.call_async(arm_request)
        future.add_done_callback(self.arm_response_callback)

    def handle_command_service(self, request, response):
        # Handle incoming requests to the command service
        self.get_logger().info(f"Received command: {request.command}, item ID: {request.item_id}")

        # Example logic to handle commands
        if request.command == "put in inventory":
            self.put_in_inventory(request.item_id)
            response.accept = f"Item {request.item_id} put in inventory."
        elif request.command == "get from inventory":
            self.get_from_inventory(request.item_id)
            response.accept = f"Item {request.item_id} retrieved from inventory."
        else:
            response.accept = "Unknown command."

        return response

    def put_in_inventory(self, item_id):
        self.get_logger().info(f'Putting item {item_id} in inventory.')
        
        command_request = Inventory.Request()
        command_request.command = 'put in inventory'
        command_request.item_id = item_id

        future = self.inventory_client.call_async(command_request)
        future.add_done_callback(self.inventory_response_callback)

    def get_from_inventory(self, item_id):
        self.get_logger().info(f'Getting item {item_id} from inventory.')
        
        command_request = Inventory.Request()
        command_request.command = 'get from inventory'
        command_request.item_id = item_id

        future = self.inventory_client.call_async(command_request)
        future.add_done_callback(self.inventory_response_callback)

    def arm_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Arm movement successful.")
            else:
                self.get_logger().warning("Arm movement failed.")
        except Exception as e:
            self.get_logger().error(f'Failed to call arm service: {e}')

    def inventory_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Received inventory response: {response.response}')
        except Exception as e:
            self.get_logger().error(f'Failed to call inventory service: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = BrainNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
