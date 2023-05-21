"""
This module handles UI and gamelogic
"""
import sys
import pyglet
from transformer import Transformer
import config
from obstacles import Obstacles

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

transformer = Transformer(video_id)

background_image = pyglet.resource.image('assets/background.png')
background_image.width = transformer.WINDOW_WIDTH
background_image.height = transformer.WINDOW_HEIGHT

window = pyglet.window.Window(
        width=transformer.WINDOW_WIDTH,
        height=transformer.WINDOW_HEIGHT)

def init():
    """
    Initializes UI elements and obstacles
    """
    global game_state, start_screen, window, shape, this_obstacles, instruction_label, score_display, end_score_label, end_label

    game_state = config.GameState.INSTRUCTION

    start_screen = pyglet.sprite.Sprite(img=background_image)

    this_obstacles = Obstacles(x_min_position = int((transformer.WINDOW_WIDTH)*0.2),
                                x_max_position = int((transformer.WINDOW_WIDTH)*0.8),
                                max_radius = 30,
                                y_window = transformer.WINDOW_HEIGHT)

    instruction_label = pyglet.text.Label(text = "Hold your AruCo Marker board in front of the webcam to start",
                                            font_size=15,
                                            x = transformer.WINDOW_WIDTH/2,
                                            y = transformer.WINDOW_HEIGHT/2,
                                            color = (0,0,0,200),
                                            anchor_x='center')

    score_display = pyglet.text.Label(text="",
                                      font_size=20,
                                      x=10,
                                      y=transformer.WINDOW_HEIGHT/2,
                                      color = config.ACCENT_COLOR)

    end_label = pyglet.text.Label(text = "Press 'R' to restart, 'Q' to quit",
                                            font_size=15,
                                            x = transformer.WINDOW_WIDTH/2,
                                            y = transformer.WINDOW_HEIGHT/3,
                                            color = (0,0,0,200),
                                            anchor_x='center')
    
    end_score_label = pyglet.text.Label(text = "",
                                            font_size=50,
                                            x = transformer.WINDOW_WIDTH/2,
                                            y = (2*transformer.WINDOW_HEIGHT)/3,
                                            color = (0,0,0,200),
                                            anchor_x='center')

    pyglet.app.run()

@window.event
def on_key_press(symbol, modifiers) -> None:
    '''
    Pyglet listener for "R" button to restart game, and "Q" button to quit game
    '''
    if symbol == pyglet.window.key.R:
        init()
    if symbol == pyglet.window.key.Q:
        pyglet.app.exit()

@window.event
def on_draw():
    """
    Handler for pyglet.windows.on_draw() event
    """
    global game_state, last_image, counter, score_display, end_score_label, end_label
    window.clear()
    if game_state == config.GameState.INSTRUCTION:
        start_screen.draw()
        instruction_label.draw()
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
        adaptive_thresh = transformer.get_finger_position(last_image.get_data())
        is_collission = this_obstacles.check_collissions(adaptive_thresh)
        score_display.text = f"{this_obstacles.score}"
        score_display.draw()
        if is_collission:
            end_score_label.text = f"{this_obstacles.score}"
            game_state = config.GameState.END
    if game_state == config.GameState.END:
        start_screen.draw()
        end_label.draw()
        end_score_label.draw()




if __name__ == '__main__':
    init()
