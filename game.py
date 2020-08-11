import json
import pygame
from board_components import inputs, outputs
from managers.GameManagers import GameManager, MenuManager, Managers, InputController
from game_objects.gui_button import GUIButton
import time
import settings
from os.path import join
from os import system
from random import shuffle


"""
This is the main game script by Vortech 2019, Extended by the The Nights Watch 2020.

It will read in the narrative.json file and operate the game logic based on that.

"""

if __name__ == "__main__":

    fps_font = pygame.font.Font(None, 32)

    # FPS settings.
    if not settings.PRODUCTION:
        
        fps_text = fps_font.render('FPS: ', True, (255,255,255)) 
        fps_textRect = fps_text.get_rect()  
        fps_textRect.center = (30, 10)

    # Get the json data
    with open("narrative.json", "r") as f:
        narrative = json.loads(f.read())

    screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
    design_canvas = pygame.Surface([settings.DESIGN_WIDTH, settings.DESIGN_HEIGHT])

    # Draw loading screen.
    loading_text = fps_font.render('Loading...', True, (255,255,255))
    loading_textRect = loading_text.get_rect()
    x, y = screen.get_size()
    loading_textRect.center = (x/2, y/2)

    screen.blit(loading_text, loading_textRect)
    pygame.display.update()


    done = False
    in_menu = True

    # Pin defintions
    FAN_PIN = 3

    # Define other constants
    DEBOUNCE_TIMER = 1

    def randomise_button_positions(buttons):
        positions = []
        ##for button in buttons:
        ##    positions.append(button["location"])

        ##shuffle(positions)

        ##for index, button in enumerate(buttons):
        ##    button["preload_button"].set_pos(positions[index])
        ##    button["location"] = positions[index]
            
        ##buttons.sort(key=lambda x : x["location"][0])


   

    # Pre-render buttons for performance.
    def preload_buttons(_dict, randomise_buttons=False):
        for item in _dict:
            buttons = item.get("buttons")
            if buttons:
                for button in buttons:
                    button["preload_button"] = GUIButton(design_canvas, button["location"], button["text"], button["effects"], None, button.get("sound_hover", None), None)
                if randomise_buttons:
                    randomise_button_positions(buttons)
                
    preload_buttons(narrative, randomise_buttons=True)
    preload_buttons(settings.menu_narrative)



    # Preload sound effects.
    def preload_sounds():
        for scene in narrative:
            for button in scene["buttons"]:
                if "effects" in button:
                    if "selected_sound" in button["effects"]:
                        if button["effects"]["selected_sound"]:
                            button["effects"]["selected_sound"] = pygame.mixer.Sound(join("assets", "SoundSelected", button["effects"]["selected_sound"]))
                    if "sound_narration" in button["effects"]:
                        if button["effects"]["sound_narration"]:
                            button["effects"]["sound_narration"] = pygame.mixer.Sound(join("assets", "SoundNarration", button["effects"]["sound_narration"]))
            if "sound_narration" in scene:
                scene["sound_narration"] = pygame.mixer.Sound(join("assets", "SoundNarration", scene["sound_narration"]))

    preload_sounds()




    # Initialise controllers.
    input_controller = InputController(debounce_time=DEBOUNCE_TIMER, debug=settings.DEBUG)
    game_manager = GameManager(narrative, design_canvas, input_controller)
    menu_manager = MenuManager(settings.menu_narrative, design_canvas, input_controller)
    managers = Managers(game_manager, menu_manager)

    # Start the gameclock.
    clock = pygame.time.Clock()


    while not done:

        # Limit the FPS to a managable speed.
        clock.tick(settings.FPS)

        # Clear the screen and design canvas to the background colour.
        screen.fill(settings.BACKGROUND_COLOUR)
        design_canvas.fill(settings.BACKGROUND_COLOUR)

        # Get the events to feed into the various objects.
        events = pygame.event.get()

        # Update the managers.
        managers.update(events)

        # Display the FPS if not in production.
        if not settings.PRODUCTION:
            fps_text = fps_font.render('FPS: ' + str(round(clock.get_fps(), 2)), True, (255,255,255)) 
            design_canvas.blit(fps_text, fps_textRect)

        # Scale the scene.
        pygame.transform.scale(design_canvas, pygame.display.get_surface().get_size(), screen)

        # Update the screen.
        pygame.display.update()

        # For debugging on pi.
        if not settings.DEBUG:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break

        # Check if we are done.
        if managers.is_complete():
            break

    pygame.quit()
    exit()
