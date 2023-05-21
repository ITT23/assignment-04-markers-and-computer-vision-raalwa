import sys
import pyglet
from transformer import Transformer
import config
from PIL import Image
import numpy as np
from obstacles import Obstacles

background_image = pyglet.resource.image('assets/background.png')

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

transformer = Transformer(video_id)

window = pyglet.window.Window(
        width=transformer.WINDOW_WIDTH,
        height=transformer.WINDOW_HEIGHT)

def init():
    global game_state, start_screen, window, shape, this_obstacles

    game_state = config.GameState.INSTRUCTION

    start_screen = pyglet.sprite.Sprite(img=background_image)

    this_obstacles = Obstacles(x_min_position = int((transformer.WINDOW_WIDTH)*0.2),
                                x_max_position = int((transformer.WINDOW_WIDTH)*0.8),
                                max_radius = 30,
                                y_window = transformer.WINDOW_HEIGHT)

    pyglet.app.run()

@window.event
def on_key_press(symbol, modifiers) -> None:
    '''
    Pyglet listener for "R" button to restart game
    '''
    if symbol == pyglet.window.key.R:
        init()
    if symbol == pyglet.window.key.S:
        check_colission(last_image.get_data())

def check_colission(image_one):
    return transformer.get_colission(image_one)

@window.event
def on_draw():
    global game_state, last_image, counter
    window.clear()
    if game_state == config.GameState.INSTRUCTION:
        start_screen.draw()
        image = transformer.get_transformed_image()
        if image is not None:
            game_state = config.GameState.START
            last_image = image
    if game_state == config.GameState.START:
        current_image = transformer.get_transformed_image()
        if current_image is not None:
            last_image = current_image
        last_image.blit(0,0,0)
        this_obstacles.update()
        adaptive_thresh = transformer.get_colission(last_image.get_data())
        is_collission = this_obstacles.check_collissions(adaptive_thresh)
        if is_collission:
            game_state = config.GameState.END
    if game_state == config.GameState.END:
        start_screen.draw()


if __name__ == '__main__':
    init()
