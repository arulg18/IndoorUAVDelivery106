import math
from collections import deque

import numpy as np
from pathfinder import RRTPathfinder


class LocalPlanner:
    END_POS_TOLERANCE_X = 10
    END_POS_TOLERANCE_Y = 10

    def __init__(self, start, destination, p_gain=0.4, i_gain=0.1, d_gain=0.06, w_gain=0.1):
        # RRT* path unusable due to the yaw state being inaccessible through the VMWare Linux machine
        # functionally, the path will work if uncommented, though it is rawer
        # since there's no explicit turns between waypoints since we can't know our absolute orientation
        #self.pathfinder = RRTPathfinder(start, destination)
        #self.path = self.pathfinder.find_path()
        self.path = [start, destination]
        print(self.path)

        self.count = -1
        #self.calculate_path_angle_for_next_waypoint()
        self.drone_pose_path_frame = None

        self.previous_error = 0.0
        self.error_sum = 0.0
        self.last_time = 0.0

        self._ring_buff_capacity = 3
        self._ring_buff = deque([], self._ring_buff_capacity)

        self.Kp = p_gain
        self.Ki = i_gain
        self.Kd = d_gain
        self.Kw = w_gain
        print("created local planner")

    def adjust_next_step(self, world_pose, curr_time):
        error = self.drone_pose_path_frame[1]  # target position - current position

        self.error_sum = self.Kw * self.error_sum + error

        dt = curr_time - self.last_time
        curr_derivative = (error - self.previous_error) / dt
        self._ring_buff.append(curr_derivative)
        ed = np.mean(self._ring_buff)

        #yaw_scale = self.Kp * error
        print("error", error)
        #print("yaw_scale", yaw_scale)

        yaw_scale = self.Kp * error + self.Kd * ed
        # yaw_scale = self.Kp * error + self.Ki * self.error_sum + self.Kd * ed

        self.previous_error = error
        self.last_time = curr_time

        return int(yaw_scale)

    def calculate_path_angle_for_next_waypoint(self):
        if self.count + 1 == len(self.path):
            self.path_angle = 0
        waypoint_y = self.path[self.count + 1][1]
        waypoint_x = self.path[self.count + 1][0]
        waypoint_y_displacement = waypoint_y - self.path[self.count][1]
        waypoint_x_displacement = waypoint_x - self.path[self.count][0]

        
        self.path_angle = math.atan(waypoint_y_displacement/waypoint_x_displacement)
        if waypoint_x_displacement < 0:
            self.path_angle += math.pi
        print("path_angle", self.path_angle)
    
    def is_next_waypoint_reached(self, world_pose):
        waypoint = self.path[self.count + 1]
        #waypoint_vec = np.array([[waypoint[0]],
                      #          [waypoint[1]]])
        waypoint_vec = waypoint

        waypoint_pose_path_frame = LocalPlanner.transform_pose_to_path_frame(waypoint_vec, self.path[self.count], self.path_angle)
        self.drone_pose_path_frame = LocalPlanner.transform_pose_to_path_frame(world_pose, self.path[self.count], self.path_angle)
        print("pos", world_pose, self.drone_pose_path_frame[0], waypoint_pose_path_frame[0])
        if waypoint_pose_path_frame[0] < 0:
            return self.drone_pose_path_frame[0] <= waypoint_pose_path_frame[0]

        return self.drone_pose_path_frame[0] >= waypoint_pose_path_frame[0]

    def next_waypoint_reached(self, drone_yaw):
        self.count += 1
        if (self.count == len(self.path) - 1):
            return 0
        self.calculate_path_angle_for_next_waypoint()

        return self.path_angle - drone_yaw

    @staticmethod
    def transform_pose_to_path_frame(pose, last_waypoint, angle):
        in_x = pose[0] - last_waypoint[0]
        in_y = pose[1] - last_waypoint[1]

        new_frame_pose = [in_x * math.cos(angle) - in_y * math.sin(angle),
                          in_x * math.sin(angle) + in_y * math.cos(angle)]

        return new_frame_pose

    @staticmethod
    def is_in_range(curr, goal):
        return abs(curr[0] - goal[0]) < LocalPlanner.END_POS_TOLERANCE_X and abs(
            curr[1] - goal[1]) < LocalPlanner.END_POS_TOLERANCE_Y

    def reached_destination(self):
        return self.count == len(self.path) - 1

    def reached_destination_radius(self, pose):
        return LocalPlanner.is_in_range(pose, self.path[-1])

