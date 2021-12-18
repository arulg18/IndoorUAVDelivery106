import rospy
from djitellopy import Tello
from movement import LocalPlanner
from geometry_msgs.msg import Pose
import numpy as np
import math


class Drone:
    """
    forward_vel: float, Forward velocity
    world_yaw: Starting yaw
    """

    def __init__(self, forward_vel, world_yaw):
        self.drone = Tello()
        self.vel = forward_vel
        self.initial_yaw = math.radians(world_yaw)
        self.start_time = 0.0
        self.r = None
        self.curr_pose = None

        self.drone.connect(False)
        rospy.sleep(5)
        rospy.on_shutdown(self.shutdown)


    """
    Takeoff procedure
    """

    def takeoff(self):
        self.drone.takeoff()
    """
    Land procedure
    """

    def land(self):
        self.drone.land()

    """
    Shutdown procedure
    """

    def shutdown(self):
        self.land()

    def start_local_planner(self, start, destination):
        self.local_planner: LocalPlanner = LocalPlanner(start, destination)

    # def start_local_planner(self, start, destination, p, i, d, w):
    #     self.local_planner: LocalPlanner = LocalPlanner(start, destination, p, i, d, w)

    def initialize_pose(self, destination):
        self.start_time = rospy.Time.now()
        self.r = rospy.Rate(10)
        self.curr_pose = rospy.wait_for_message("unfiltered_pose", Pose)

        # self.curr_pose = None
        # while self.curr_pose is None:
        #     try:
        #         self.curr_pose = rospy.wait_for_message("unfiltered_pose", Pose, timeout=10)
        #     except:
        #         pass

        xy_pose = (self.curr_pose.position.x, self.curr_pose.position.y)
        # Create local planner object and find path to destination from start
        self.start_local_planner(xy_pose, destination)
        self.listener()

    def callback(self, message):
        self.curr_pose = message

    def listener(self):
        rospy.Subscriber("unfiltered_pose", Pose, self.callback)

    """
    Execute 2D path plan at hover height from start to destination coordinates
    """

    def execute_path_plan(self, timeout_secs=60):
        first = True
        while not rospy.is_shutdown():
            t = (rospy.Time.now() - self.start_time).to_sec()

            if timeout_secs is not None and t >= timeout_secs:
                break

            pose = [self.curr_pose.position.x, self.curr_pose.position.y]
            print("pose", pose)

            if not first and not self.local_planner.is_next_waypoint_reached(pose):
                yaw_input = self.local_planner.adjust_next_step(pose, t)

                self.drone.send_rc_control(0, self.vel, 0, yaw_input)

                if self.local_planner.reached_destination_radius(pose):
                    print("in radius, landing")
                    break

            else:
                angle = int(math.degrees(self.local_planner.next_waypoint_reached(self.initial_yaw)))
                if self.local_planner.reached_destination():
                    print("path complete, landing")
                    break

                print("angle to turn", angle)
                if angle > 0:
                    self.drone.rotate_counter_clockwise(angle)
                elif angle < 0:
                    self.drone.rotate_clockwise(abs(angle))
                first = False
            self.r.sleep()
        self.drone.send_rc_control(0, 0, 0, 0)
        self.land()
