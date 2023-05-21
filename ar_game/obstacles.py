"""
This module manages obstacles for the game
"""
import pyglet
import config
import random

class Obstacles:
    def __init__(self, x_min_position, x_max_position, max_radius, y_window):
        """
        Sets up boundaries for obstacle creation
        """
        self.obstacles = []
        self.x_min_position = x_min_position
        self.x_max_position = x_max_position
        self.y_window = y_window
        self.max_radius = max_radius
        self.score = 0
        self.number_of_obstacles = 0

    def update(self):
        """
        Creates obstacles when needed, moves them downwards and renders all of them
        """
        if not self.obstacles:
            self.create_obstacle()
        for obstacle in self.obstacles:
            obstacle.y -= 5
            obstacle.draw()
        if self.obstacles[-1].y < (self.y_window/5)*4:
            self.create_obstacle()
        if len(self.obstacles) < self.number_of_obstacles:
            self.score +=1
            self.number_of_obstacles = len(self.obstacles)

    def create_obstacle(self):
        """
        Creates obstacle within boundaries and appends it to obstacle list
        """
        obstacle = pyglet.shapes.Circle(x=random.randint(self.x_min_position, self.x_max_position),
                                        y = self.y_window,
                                        radius = random.randint(10, self.max_radius),
                                        color = config.TEXT_COLOR)
        self.obstacles.append(obstacle)
        self.number_of_obstacles = len(self.obstacles)

    def check_collissions(self, finger_matrix):
        """
        Checks if finger touches obstacle and if obstacle was missed
        If the finger hit an obstacle, it is deleted and removed from obstacle list

        Returns:
            True if obstacle was missed and game is over

            False if game over condition is not met
        """
        for obstacle in self.obstacles:
            if (obstacle.y + obstacle.radius) <= 0:
                return True
            if finger_matrix[int(obstacle.y)-1][int(obstacle.x)-1] == 0:
                self.obstacles.remove(obstacle)
                obstacle.delete()
        return False
