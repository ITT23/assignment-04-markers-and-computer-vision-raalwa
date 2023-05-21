import sys
import pyglet
from transformer import Transformer
import config
from PIL import Image
import numpy as np

background_image = pyglet.resource.image('assets/background.png')

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

transformer = Transformer(video_id)

window = pyglet.window.Window(
        width=transformer.WINDOW_WIDTH,
        height=transformer.WINDOW_HEIGHT)

def init():
    global game_state, start_screen, window, shape

    game_state = config.GameState.INSTRUCTION

    start_screen = pyglet.sprite.Sprite(img=background_image)

    shape = pyglet.shapes.Circle(x=10,y=10,radius=50, color = (255,215,0))

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
        adaptive_thresh = transformer.get_colission(last_image.get_data())
        adaptive_thresh = np.flip(adaptive_thresh, 0)
        if adaptive_thresh[int(shape.y)][int(shape.x)] == 0:
            print("Collission")
    shape.draw()


if __name__ == '__main__':
    init()
