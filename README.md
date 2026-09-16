# ROS 2 pick-and-place cell

UNSW **MTRN4231** (Robotics, 2024 T3) coursework: a ROS 2 workspace for a simulated pick-and-place cell. A camera reports detected items, an operator issues pick/place commands, inventory tracks three slots, and a simulated arm service executes motion.

This is a snapshot of my solution from the private GitHub Classroom repo. Course assignment PDFs are not included.

## Architecture

| Package | What it does |
| --- | --- |
| `interfaces` | Custom messages and services (`BrainStatus`, `InventoryStatus`, `Command`, `Inventory`, plus provided `Camera` / `ArmMovement`) |
| `inventory` | Three-slot store: put/get items and publish slot status; TF for slot frames |
| `perception` | Subscribe to simulated camera detections, broadcast item TFs, publish the last five unique item IDs |
| `brain` | Operator command service, coordinates inventory and arm, system launch |
| `arm` | Provided simulated arm movement service |

## Build (ROS 2)

From the workspace root (this repository):

```bash
./compile.sh
```

That builds `interfaces` first, sources the overlay, then builds the remaining packages with `colcon`.

Launch the full cell:

```bash
source install/setup.bash
ros2 launch brain system_launch.py
```

Individual packages also have launch files under `src/<package>/launch/`.

## Stack

ROS 2 · Python · `colcon` · `tf2_ros` · custom ROS interfaces
