# UAV_hoist_Gazebo

A Gazebo simulation environment tailored for UAV  lifting and hoisting operations.   
This project is a refactored version of the [PX4-ROS2-Gazebo-Drone-Simulation-Template](https://github.com/SathanBERNARD/PX4-ROS2-Gazebo-Drone-Simulation-Template.git). It has been specifically adapted for PX4 v1.16.1 and includes critical bug fixes and a new simulation world.

## Key Features

*   **PX4 v1.16.1 Compatibility:** The core simulation world (`test_world.sdf`) has been refactored and adapted to align with the official PX4 v1.16.1 Gazebo template.
*   **Resolved Sensor Issues:** Fixed the "Found 0 compass" error in QGroundControl (QGC) and the issue where no data was published on the `/fmu/out/vehicle_local_position` topic.
*   **Custom Simulation World:** Introduced a new world that integrates the `basketball_court.sdf` model.

## System Requirements

| Component | Version |
| :--- | :--- |
| Ubuntu | 22.04 |
| ROS 2 | Humble |
| PX4 Autopilot | 1.16.1 |
| px4_msgs & px4_ros_com | release/1.16 |
| Micro-XRCE-DDS-Agent | 3.0.1 |