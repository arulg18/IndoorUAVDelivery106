import math
from collections import deque

import numpy as np
from drone_localization.src.delivery.src.controls.pathfinder import RRT_Pathfinder


class LocalPlanner:
    END_POS_TOLERANCE_X = 5
    END_POS_TOLERANCE_Y = 5
    END_POS_TOLERANCE_Z = 5

    def __init__(self, start, destination, p_gain=0.2, i_gain=0.1, d_gain=0.01, w_gain=0.9):
        self.pathfinder = RRT_Pathfinder(start, destination)
        self.path = self.pathfinder.find_path()[1]
        self.count = 0
        self.calculate_path_angle_for_next_waypoint()
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

    def adjust_next_step(self, world_pose, curr_time):
        error = self.drone_pose_path_frame[1]  # target position - current position

        self.error_sum = self.Kw * self.error_sum + error

        dt = curr_time - self.last_time
        curr_derivative = (error - self.previous_error) / dt
        self._ring_buff.append(curr_derivative)
        ed = np.mean(self._ring_buff)

        yaw_scale = self.Kp * error + self.Ki * self.error_sum + self.Kd * ed

        self.previous_error = error
        self.last_time = curr_time

        return yaw_scale

    def calculate_path_angle_for_next_waypoint(self):
        if self.count + 1 == len(self.path):
            self.path_angle = 0
        waypoint_y = self.path[self.count + 1][1]
        waypoint_x = self.path[self.count + 1][0]
        waypoint_y_displacement = waypoint_y - self.path[self.count][1]
        waypoint_x_displacement = waypoint_x - self.path[self.count][0]

        self.path_angle = np.arctan([waypoint_x_displacement, waypoint_y_displacement])

    def is_next_waypoint_reached(self, world_pose):
        waypoint = self.path[self.count + 1]
        waypoint_vec = np.array([waypoint[0]],
                                [waypoint[1]])

        waypoint_pose_path_frame = self.transform_pose_to_path_frame(waypoint_vec)
        self.drone_pose_path_frame = self.transform_pose_to_path_frame(world_pose)
        return self.drone_pose_path_frame[0] >= waypoint_pose_path_frame[0]

    def next_waypoint_reached(self, drone_yaw) -> int:
        self.count += 1
        self.calculate_path_angle_for_next_waypoint()

        return self.path_angle - drone_yaw # TODO: think about like 360 vs 180 and shit

    def transform_pose_to_path_frame(self, current_pos):
        inv_rotation_matrix = np.array(
            [[np.cos(self.path_angle), np.sin(self.path_angle)], [-np.sin(self.path_angle), np.cos(self.path_angle)]])
        int_matrix = np.subtract(current_pos, np.transpose([self.path[self.count][0], self.path[self.count][1]]))
        output_transform = np.multiply(inv_rotation_matrix, int_matrix)

        return output_transform

    @staticmethod
    def is_in_range(curr, goal):
        return abs(curr[0] - goal[0]) < LocalPlanner.END_POS_TOLERANCE_X and abs(
            curr[1] - goal[1]) < LocalPlanner.END_POS_TOLERANCE_Y and abs(
            curr[1] - goal[1]) < LocalPlanner.END_POS_TOLERANCE_Z

    def reached_destination(self):
        return self.count == len(self.path)  # TODO maybe add special functionality for destination checking, none for now
