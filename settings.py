from subprocess import call
from platform import uname
import pygame

# Initialise pygame assets.
pygame.init()

# Set the mouse to invisible.
pygame.mouse.set_visible(False)

SYSTEM = uname().system

# If running on the pi it will be Linux.
DEBUG = False if SYSTEM == "Linux" else True
PRODUCTION = True
FONT_SIZE = 100
BACKGROUND_COLOUR = (0, 0, 0)
FPS = 10
LABEL_COLOUR = (255,255,0,100)
SELECTED_COLOUR = (255, 0, 0, 100)
DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
BUTTON_MIN_ZOOM = 200
BUTTON_MAX_ZOOM = 60
BUTTON_ZOOM_RATE = 10
MESSAGE_LOCATION = (480, 960)
MESSAGE_TIMER = 5.0
CYCLE_BUTTON_TIMER = 2.0
# Set channels.
pygame.mixer.set_num_channels(3)
NARRATION = pygame.mixer.Channel(0)
SELECTED_EFFECTS = pygame.mixer.Channel(1)
SOUND_EFFECTS = pygame.mixer.Channel(2)
TRANSITION_SOUND = pygame.mixer.Sound("assets/bell.wav")
SELECTED_SOUND = pygame.mixer.Sound("assets/selected.wav")

# Pins
## Outputs
FAN = 26
VIBE_MAT = 19
ROTORS = 13
CUSTOM = 6

## Inputs
BUTTON_ONE = 16
BUTTON_TWO = 20
SHUTDOWN = 21

# Durations for outputs
FAN_PULSE_DURATION = 1
FAN_PULSE_TOTAL = 3
FAN_PULSE_INTERVAL = 2
ROTORS_PULSE_DURATION = 1
ROTORS_PULSE_TOTAL = 4
ROTORS_PULSE_INTERVAL = .5
VIBE_MAT_PULSE_DURATION = 1
VIBE_MAT_PULSE_TOTAL = 3
VIBE_MAT_PULSE_INTERVAL = 1
CUSTOM_PULSE_DURATION = 3
CUSTOM_PULSE_TOTAL = 2
CUSTOM_PULSE_INTERVAL = 1

# This is the narrative structure for the menu.

# FUNCTIONS FOR NARRATIVE


def shutdown():
    pygame.quit()
    if SYSTEM == "Linux":
        call("clear", shell=True)
        call("sudo shutdown -h now", shell=True)



menu_narrative = [

    {
        "title": "Welcome to the adventure!",
        "not_random": "Yes",
        "buttons": [
            {
                "image": "assets/img/buttons/start.png",
                "frames" : 4,
                "location": [560, 720],
                "text": "Start",
                "effects": {
                    "not_random": "Yes",
                    "manager": "having this key will swap the manager. This value doesnt matter."
                }
            },
            {
                "image": "assets/img/buttons/options.png",
                "frames" : 4,
                "location": [960, 720],
                "text": "Options",
                "effects": {
                    "not_random": "Yes",
                    "goto": 1
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1360, 720],
                "text": "Shutdown",
                "effects": {
                    "not_random": "Yes",
                    "plain_function": shutdown
                }
            }


        ]
    },
    {
        "title": "Difficulty",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 720],
                "text": "Easy",
                "effects": {
                    "not_random": "Yes",
                    "mode": "easy",
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 720],
                "text": "Advanced",
                "effects": {
                    "not_random": "Yes",
                    "mode": "adv",
                    "goto": 0
                }
            }


        ]
    }
]
