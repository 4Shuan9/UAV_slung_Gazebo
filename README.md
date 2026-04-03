# UAV_slung_Gazebo

A Gazebo simulation environment tailored for UAV with a slung payload operations.   
This project is a refactored version of the [rain_ws](https://github.com/RainbowSeeker/rain_ws.git) & [PX4-ROS2-Gazebo-Drone-Simulation-Template](https://github.com/SathanBERNARD/PX4-ROS2-Gazebo-Drone-Simulation-Template.git). It has been specifically adapted for PX4 v1.16.1 and includes critical bug fixes and a new simulation world.

## Key Features

* **PX4 v1.16.1 Compatibility:** Fully refactored the core simulation world (`test_world.sdf`) to align seamlessly with the official PX4 v1.16.1 Gazebo templates.
* **Enhanced Tether & Payload Dynamics:** Redesigned the tether mechanism by discretizing a 1-meter string into 20 articulated segments, and optimized the payload model to achieve highly realistic slung-load physics.
* **Dedicated Simulation Environments:** Built specialized simulation worlds tailored exclusively for slung-payload experiments, including the integration of a custom `basketball_court.sdf` model.
* **Resolved Sensor & Telemetry Issues:** Fixed the "Found 0 compass" error in QGroundControl (QGC) and restored missing data publications on the `/fmu/out/vehicle_local_position` topic.

## System Requirements

| Component | Version |
| :--- | :--- |
| Ubuntu | 22.04 |
| ROS 2 | Humble |
| PX4 Autopilot | 1.16.1 |
| px4_msgs & px4_ros_com | release/1.16 |
| Micro-XRCE-DDS-Agent | 3.0.1 |

## Quick Start Guide
```
# Launch QGroundControl (QGC)
cd ~/Desktop
./QGroundControl_5.0.8.AppImage

# Start the Micro-XRCE-DDS Agent
MicroXRCEAgent udp4 -p 8888

# Launch the Gazebo Simulation World
gz sim -r UAV_slung_world.sdf

# Start PX4 SITL
cd ~/PX4-Autopilot
export PX4_GZ_MODEL_NAME=x500_mono_cam_down
./build/px4_sitl_default/bin/px4

# Start the Downward Camera Node
ros2 run slung_ctrl gz_cam_raw

# Start the ROS-GZ Bridge for the Payload IMU
ros2 run ros_gz_bridge parameter_bridge /world/UAV_slung_world/model/payload_ball/link/ball_link/sensor/ball_imu/imu@sensor_msgs/msg/Imu[gz.msgs.IMU

# Echo data from the payload's IMU
ros2 topic echo /world/UAV_slung_world/model/payload_ball/link/ball_link/sensor/ball_imu/imu

# Command the UAV to Takeoff
ros2 run slung_ctrl slung_takeoff
```