import numpy as np

from rrt_star import RRTStar
from search_space import SearchSpace


class RRTPathfinder:
    Obstacles = np.array([])
    X_dimensions = np.array([(0, 500), (0, 500)])
    Q = np.array([(2, 1)])  # length of tree edges
    r = .1  # length of smallest edge to check for intersection with obstacles
    max_samples = 1024  # max number of samples to take before timing out
    rewire_count = 32  # optional, number of nearby branches to rewire
    prc = 0.001  # probability of checking for a connection to goal

    # create Search Space
    X = SearchSpace(X_dimensions, Obstacles)

    def __init__(self, x_init, x_goal):
        self.rrt_star_handler = RRTStar(RRTPathfinder.X, RRTPathfinder.Q, x_init, x_goal, RRTPathfinder.max_samples,
                                        RRTPathfinder.r, RRTPathfinder.prc, RRTPathfinder.rewire_count)

    def find_path(self):
        return self.rrt_star_handler.rrt_star()
