#!/usr/bin/env python3
# from src.controls.movement import Drone
#
# my_drone = Drone()
# tello = my_drone.get_drone()
# tello.takeoff()
#
# currentPos = [0,0,0]
# x_init = (0, 0, 0)
# x_goal = (100, 100, 100)
# count = 0
# currentError = 0 # should we start at 0?
# orientation = 0 # from YAW
#
# my_drone.set_new_path(x_init, x_goal)
#
# while not my_drone.is_in_range(currentPos,x_goal):
#     while not my_drone.is_in_range(currentPos, my_drone.get_next_waypoint(count)):
#         my_drone.adjust(currentPos, currentError,orientation)
#     count +=1
#     my_drone.generate_local_line(my_drone.get_next_waypoint(count-1),my_drone.get_next_waypoint(count),orientation)
#

from drone import Drone
import rospy
from geometry_msgs.msg import Pose


if __name__ == '__main__':
    rospy.init_node('executor', anonymous=True)

    destination = (136, 255)

    drone = Drone(10, 90)
    rospy.sleep(10)

    drone.takeoff()
    rospy.sleep(3)

    drone.initialize_pose(destination)

    drone.execute_path_plan()

