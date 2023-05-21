import pyglet
import config
import random

class Obstacles:
    def __init__(self, x_min_position, x_max_position, max_radius, y_window):
        self.obstacles = []
        self.x_min_position = x_min_position
        self.x_max_position = x_max_position
        self.y_window = y_window
        self.max_radius = max_radius

    def update(self):
        if not self.obstacles:
            self.create_obstacle()
        for obstacle in self.obstacles:
            obstacle.y -= 5
            obstacle.draw()
        if self.obstacles[-1].y < (self.y_window/5)*4:
            self.create_obstacle()

    def create_obstacle(self):
        obstacle = pyglet.shapes.Circle(x=random.randint(self.x_min_position, self.x_max_position),
                                        y = self.y_window,
                                        radius = random.randint(10, self.max_radius),
                                        color = (255,215,0))
        self.obstacles.append(obstacle)

    def check_collissions(self, finger_matrix):
        for obstacle in self.obstacles:
            if (obstacle.y + obstacle.radius) <= 0:
                return True
            if finger_matrix[int(obstacle.y)-1][int(obstacle.x)-1] == 0:
                self.obstacles.remove(obstacle)
                obstacle.delete()
        return False
