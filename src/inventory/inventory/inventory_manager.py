import rclpy
from rclpy.node import Node
from interfaces.srv import Inventory  # Import your Inventory service
from interfaces.msg import InventoryStatus  # Import your InventoryStatus message
from std_msgs.msg import Int32MultiArray  # If you're using this for inventory status


class InventoryManager(Node):
    def __init__(self):
        super().__init__('inventory_manager')

        # Internal state of the inventory (3 slots)
        self.inventory_slots = [-1, -1, -1]  # -1 represents empty slots

        # Service to handle inventory commands
        self.srv = self.create_service(Inventory, 'inventory', self.handle_inventory)

        # Publisher for inventory status
        self.inventory_status_pub = self.create_publisher(InventoryStatus, 'inventory_status', 1)

        # Timer to periodically publish inventory status
        self.timer = self.create_timer(1.0, self.publish_inventory_status)

    def handle_inventory(self, request, response):
        command = request.command
        item_id = request.item_id
    
        if command == "put in inventory":
            response.response = self.put_in_inventory(item_id)
        elif command == "get from inventory":
            response.response = self.get_from_inventory(item_id)
        else:
            response.response = -2  # Invalid command
        return response

    def put_in_inventory(self, item_id):
        # Check for available slots
        for i in range(len(self.inventory_slots)):
            if self.inventory_slots[i] == -1:  # Slot is empty
                self.inventory_slots[i] = item_id
                self.get_logger().info(f'Added item {item_id} to inventory slot {i + 1}')
                return i + 1  # Return slot number (1-based index)
        self.get_logger().info('Inventory is full')
        return -1  # Inventory full

    def get_from_inventory(self, item_id):
        # Find the item in the inventory
        for i in range(len(self.inventory_slots)):
            if self.inventory_slots[i] == item_id:
                self.inventory_slots[i] = -1  # Remove the item
                self.get_logger().info(f'Removed item {item_id} from inventory slot {i + 1}')
                return i + 1  # Return slot number (1-based index)
        self.get_logger().info(f'Item {item_id} not found in inventory')
        return -1  # Item not found

    def publish_inventory_status(self):
        msg = InventoryStatus()
        msg.slot_1 = self.inventory_slots[0]
        msg.slot_2 = self.inventory_slots[1]
        msg.slot_3 = self.inventory_slots[2]
        self.inventory_status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = InventoryManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
