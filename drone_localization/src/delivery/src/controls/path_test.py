
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

# TODO: ROSIFY this
from src.controls.drone import Drone
import rospy

# TODO parameterize yaw, start, dest as an input on runtime?
#  start technically is based on drone, so that shouldn't be parametrized
parameterized_yaw = None
start = None
dest = None

drone = Drone(10, parameterized_yaw)
rospy.sleep(0.5)

drone.takeoff()
drone.execute_path_plan(start, dest, None)