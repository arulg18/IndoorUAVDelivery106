import numpy as np

from src.rrt.rrt_star import RRTStar
from src.search_space.search_space import SearchSpace

class RRT_Pathfinder:
    Obstacles = np.array(
        [(20, 20, 20, 40), (20, 20, 60, 40), (20, 60, 20, 40), (60, 60, 20, 80),
         (60, 20, 20, 80), (60, 20, 60, 80), (20, 60, 60, 40), (60, 60, 60, 80)])
    X_dimensions = np.array([(0, 500), (0, 500)])
    Q = np.array([(2, 1)])  # length of tree edges
    r = .1  # length of smallest edge to check for intersection with obstacles
    max_samples = 1024  # max number of samples to take before timing out
    rewire_count = 32  # optional, number of nearby branches to rewire
    prc = 0.001  # probability of checking for a connection to goal

    # create Search Space
    X = SearchSpace(X_dimensions, Obstacles)

    def __init__(self, x_init, x_goal):
        self.rrt_star_handler = RRTStar(RRT_Pathfinder.X, RRT_Pathfinder.Q, x_init, x_goal, RRT_Pathfinder.max_samples, RRT_Pathfinder.r, RRT_Pathfinder.prc, RRT_Pathfinder.rewire_count)

    def find_path(self):
        return self.rrt_star_handler.rrt_star()