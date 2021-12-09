import rospy
from djitellopy import Tello
from drone_localization.src.delivery.src.controls.movement import LocalPlanner


class Drone:
    """
    forward_vel: float, TODO: range here
    world_yaw: int TODO description
    """

    def __init__(self, forward_vel , world_yaw):
        self.drone = Tello()
        self.vel = forward_vel
        self.initial_yaw = world_yaw

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

    def start_local_planner(self, start, destination, p, i, d, w):
        self.local_planner: LocalPlanner = LocalPlanner(start, destination, p, i, d, w)

    """
    Execute 2D path plan at hover height from start to destination coordinates
    """

    def execute_path_plan(self, start, destination, timeout_secs=60):
        start_time = rospy.Time.now()
        r = rospy.Rate(10)

        # Create local planner object and find path to destination from start
        self.start_local_planner(start, destination)
        self.initial_yaw = self.drone.get_yaw()

        while not rospy.is_shutdown():
            t = (rospy.Time.now() - start_time).to_sec()

            if timeout_secs is not None and t >= timeout_secs:
                break

            # TODO: curr_pose = convertToFormat(ros.subscribe)
            curr_pose = None

            if not self.local_planner.is_next_waypoint_reached(curr_pose):
                yaw_input = self.local_planner.adjust_next_step(curr_pose, t)

                self.drone.send_rc_control(self.vel, 0, 0, yaw_input)
                r.sleep()
            else:
                angle = self.local_planner.next_waypoint_reached(self.drone.get_yaw() + self.initial_yaw)
                if self.local_planner.reached_destination():
                    break
                if angle > 0:
                    self.drone.rotate_counter_clockwise(angle)
                    # rospy.sleep() TODO check if needed then remove
                elif angle < 0:
                    self.drone.rotate_clockwise(abs(angle))
                    # rospy.sleep() TODO check if needed then remove
                r.sleep()

        self.land()

