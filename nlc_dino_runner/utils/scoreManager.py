

class ScoreManager:
    def __init__(self):
        self.death_count = 0
        self.points = 0
        self.max_score = 0
        self.max_points = 0

    def update_points(self):
        self.points += 1

    def update_at_the_end(self):
        self.max_score = self.points
        self.max_points = max(self.max_points, self.points)
        self.points = 0
