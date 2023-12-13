class Solution:
    def __init__(self):
        self.path = []
        self.z = []
        self.time = -1.0
        self.profit = -1.0
        self.weight = -1.0
        self.single_objective = -1.0
        self.objectives = []

    def get_relation(self, other):
        val = 0
        for i in range(len(self.objectives)):
            if self.objectives[i] < other.objectives[i]:
                if val == -1:
                    return 0
                val = 1
            elif self.objectives[i] > other.objectives[i]:
                if val == 1:
                    return 0
                val = -1
        return val

    def equals_in_design_space(self, other):
        return self.path == other.path and self.z == other.z



