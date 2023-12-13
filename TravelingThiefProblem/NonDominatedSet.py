class NonDominatedSet:
    def __init__(self):
        # entries of the non-dominated set
        self.entries = []

    # Filtering results to generate non-dominated sets
    def add(self, s):
        is_added = True

        for other in self.entries[:]:
            rel = s.get_relation(other)

            # if dominated by or equal in design space
            if rel == -1 or (rel == 0 and s.equals_in_design_space(other)):
                is_added = False
                break
            elif rel == 1:
                self.entries.remove(other)

        if is_added:
            self.entries.append(s)

        return is_added
