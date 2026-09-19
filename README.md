> **Public case study.** UNSW MTRN4231 coursework snapshot. Assignment PDFs not included.

---

## Problem statement

The course needed a **multi-node robot cell** that still made sense when the camera and arm were **simulated**. the learning target was architecture and interfaces, not tuning a single monolithic script.

## High-level impact

1. **ROS 2** workspace with **Perception, Brain, Inventory, Arm** roles and shared **interfaces** package.
2. **TF-backed** spatial model for items, slots, and arm/camera frames.
3. Operator **put/get/pick** flows via services, not ad hoc topic spaghetti.

## My contribution

1. Designed and implemented the **brain coordinator**, **inventory node**, and **perception** pipeline for the simulated cell.
2. Defined **custom messages/services** and launch/bring-up flow for integrated demos.
3. Documented cell behaviour for course submission and portfolio.

## Tech and design choices

| Choice | Why |
| --- | --- |
| **ROS 2 services for commands** | Put/get/pick need acknowledgement; topics alone hide failure modes. |
| **Separate `interfaces` package** | One schema change propagates cleanly. mirrors real integrator workflows. |
| **Simulated arm latency** | Exercises async client logic without lab hardware contention. |
| **TF for all spatial relationships** | RViz-visible cell; avoids hard-coded poses in every node. |

## Lesson

**Race conditions** appeared when perception published faster than inventory updated. Fixed by making the **brain** the sole orchestrator for pick/place sequences and tightening service call ordering instead of letting multiple nodes infer state from topics independently.

---

# ROS 2 pick-and-place cell

A small factory cell in software: detect an item, decide what to do with it, park it in inventory, or send the arm to fetch it again.

Built for **UNSW MTRN4231** (Robotics, 2024 T3) as a multi-package **ROS 2** workspace. Camera detections and arm motion are **simulated** so the focus stays on architecture, interfaces, and coordination. the same patterns you need when the hardware is real.

Public snapshot of my classroom solution. Course assignment PDFs are not included.

---

## What is happening

Think of four roles talking over ROS topics and services:

```text
  Operator ──Command.srv──▶ Brain ──Inventory.srv──▶ Inventory (3 slots)
                              │
                              ├──ArmMovement.srv──▶ Arm (simulated delay)
                              │
                              └── listens to ──▶ Perception ◀── Camera.msg
                                                     │
                                                     └── publishes item TFs + recent IDs
```

1. **Perception** watches a simulated camera stream (`Camera.msg`: item id + x/y/z).  
   Each new detection gets a TF frame (`camera_link` → `item_<id>`). Every second it publishes the last five unique item IDs on `perception_status`.

2. **Brain** is the dispatcher.  
   It exposes a `Command` service so an operator can say “put this item in inventory” or “get it back out.” It also watches brain/perception status and asks the arm to `search` or `pick` when inventory looks empty or an item shows up.

3. **Inventory** is a three-slot shelf in memory (`-1` = empty).  
   Put/get requests return the slot number (or failure). Slot state is published on a timer as `InventoryStatus`. Static TFs place `inventory_slot_1..3` relative to `base_link`.

4. **Arm** (provided simulator) accepts `ArmMovement` requests with a command and pose, sleeps for a few seconds, then returns `success`. No real kinematics. just a stand-in for motion time.

Underneath, **TF** holds the cell together: `map` → `base_link` → `arm_link` / `camera_link` / inventory slots, plus dynamic frames for whatever the camera last saw. That is what you would open in RViz to see the scene.

---

## How the packages map to that story

| Package | Job |
| --- | --- |
| `interfaces` | Shared language: custom `.msg` / `.srv` so every node agrees on fields |
| `perception` | Turn camera hits into TFs + a shortlist of recent item IDs |
| `inventory` | Own the three slots, answer put/get, publish status + slot frames |
| `brain` | Operator commands, service clients to inventory & arm, system launch |
| `arm` | Simulated move service (course-provided) |
| `interface_verification` | Course test helpers for the interfaces |

---

## Operator loop (happy path)

```text
pick request  →  Brain calls Inventory "get from inventory"
              →  Brain calls Arm "pick" at a pose
              →  Arm waits, returns success
              →  Inventory slot clears / status updates

place request →  Brain calls Inventory "put in inventory"
              →  item lands in first free slot
              →  InventoryStatus shows which slot filled
```

Perception keeps feeding the brain a rolling view of what has been “seen,” so the coordinator can react when something new appears. without embedding camera logic inside the arm or inventory nodes.

---

## Why it is split this way

ROS pays off when each concern is a node with a clear contract:

1. **Interfaces first**. change a message once; every package stays compatible  
2. **Services for actions**. put/get/pick are request–response, not fire-and-forget topics  
3. **Topics for status**. inventory and perception broadcast what they know on a timer  
4. **TF for space**. slots, camera, and items share one frame tree instead of hard-coded magic numbers in every file  

That is the same habit you want on a real cell: swap a camera driver or a real arm driver later, keep the brain and inventory contracts.

---

## Build & run

ROS 2 + Python. From the workspace root:

```bash
./compile.sh          # builds interfaces first, then the rest with colcon
source install/setup.bash
ros2 launch brain system_launch.py
```

Bring up one package at a time with the launch files under `src/<package>/launch/` if you are debugging a single node.

---

## Stack

**ROS 2** · **Python / rclpy** · **colcon** · **tf2** (static + dynamic) · **custom messages & services** · **launch files**

---

## Honest scope

This is **coursework architecture**, not a deployed robot. There is no OpenCV pipeline, no MoveIt planning, and no physical manipulator in this repo. The interesting part is the **cell design**: who owns state, how commands flow, and how perception, inventory, and motion stay loosely coupled.
