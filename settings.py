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
FPS = 12
LABEL_COLOUR = (255,255,0,100)
SELECTED_COLOUR = (255, 0, 0, 100)
DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
BUTTON_MIN_ZOOM = 200
BUTTON_MAX_ZOOM = 60
BUTTON_ZOOM_RATE = 10
MESSAGE_LOCATION = (960, 960)
MESSAGE_TIMER = 5.0
INITIAL_CYCLE_TIMER = 3
CYCLE_BUTTON_TIMER = INITIAL_CYCLE_TIMER
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
    #if SYSTEM == "Linux":
        #call("clear", shell=True)
        #call("sudo shutdown -h now", shell=True)



menu_narrative = [

    { #0
        "title": "Welcome to the adventure!",
        "not_random": "Yes",
        "buttons": [
            {
                "image": "assets/img/buttons/start.png",
                "frames" : 4,
                "location": [450, 530],
                "text": "Start",
                "effects": {
                    "not_random": "Yes",
                    "manager": "having this key will swap the manager. This value doesnt matter."
                }
            },
            {
                "image": "assets/img/buttons/options.png",
                "frames" : 4,
                "location": [960, 700],
                "text": "Options",
                "effects": {
                    "not_random": "Yes",
                    "goto": 1
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1470, 530],
                "text": "Shutdown",
                "effects": {
                    "not_random": "Yes",
                    "plain_function": shutdown
                }
            }
        ]
    },
    { #1
        "title": "Options",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [300, 620],
                "text": "Difficulty",
                "effects": {
                    "not_random": "Yes",
                    "goto": 2

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [720, 620],
                "text": "Speed",
                "effects": {
                    "not_random": "Yes",
                    "goto": 3
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1120, 620],
                "text": "Story",
                "effects": {
                    "not_random": "Yes",
                    "goto": 4
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1580, 620],
                "text": "Text",
                "effects": {
                    "not_random": "Yes",
                    "goto": 8
                }
            }
        ]
    },
    { #2
        "title": "Difficulty",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [600, 620],
                "text": "1 Switch",
                "effects": {
                    "not_random": "Yes",
                    "mode": "easy",
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1220, 620],
                "text": "2 Switch",
                "effects": {
                    "not_random": "Yes",
                    "mode": "adv",
                    "goto": 0
                }
            }
        ]
    },
    { #3
        "title": "Speed",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 620],
                "text": "Slower(+1)",
                "effects": {
                    "not_random": "Yes",
                    "speedChange": 0.5,
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 620],
                "text": "Reset("+str(INITIAL_CYCLE_TIMER)+")",
                "effects": {
                    "not_random": "Yes",
                    "speedReset": INITIAL_CYCLE_TIMER,
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1510, 620],
                "text": "Faster(-0.5)",
                "effects": {
                    "not_random": "Yes",
                    "speedChange": -0.25,
                    "goto": 0
                }
            }
        ]
    },
    { #4
        "title": "Story",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 620],
                "text": "Beginning",
                "effects": {
                    "not_random": "Yes",
                    "goto": 5

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 620],
                "text": "Middle",
                "effects": {
                    "not_random": "Yes",
                    "goto": 6
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1510, 620],
                "text": "End",
                "effects": {
                    "not_random": "Yes",
                    "goto": 7
                }
            }
        ]
    },
    { #5
        "title": "Beginning",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 620],
                "text": "Option 1",
                "effects": {
                    "not_random": "Yes",
                    "beginningOption": 1,
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1410, 620],
                "text": "Option 2",
                "effects": {
                    "not_random": "Yes",
                    "beginningOption": 2,
                    "goto": 0
                }
            }
        ]
    },
    { #6
        "title": "Middle",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 620],
                "text": "Option 1",
                "effects": {
                    "not_random": "Yes",
                    "middleOption": 1,
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1410, 620],
                "text": "Option 2",
                "effects": {
                    "not_random": "Yes",
                    "middleOption": 2,
                    "goto": 0
                }
            }
        ]
    },
    { #7
        "title": "End",
        "not_random": "Yes",
        "background_img": "assets/img/backgrounds/ocean_main.jpg",
        "buttons": [
            {
                "image": "assets/img/buttons/onebutton.png",
                "frames" : 4,
                "location": [510, 620],
                "text": "Option 1",
                "effects": {
                    "not_random": "Yes",
                    "endOption": 1,
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1410, 620],
                "text": "Option 2",
                "effects": {
                    "not_random": "Yes",
                    "endOption": 2,
                    "goto": 0
                }
            }
        ]
    },
    { #8
        "title": "Text Size",
        "not_random": "Yes",
        "buttons": [
            {
                "image": "assets/img/buttons/start.png",
                "frames" : 4,
                "location": [450, 620],
                "text": "Default",
                "effects": {
                    "not_random": "Yes",
                    "fontSize": FONT_SIZE,
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/options.png",
                "frames" : 4,
                "location": [960, 620],
                "text": "Bigger",
                "effects": {
                    "not_random": "Yes",
                    "fontSize": FONT_SIZE+30,
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1470, 620],
                "text": "Biggest",
                "effects": {
                    "not_random": "Yes",
                    "fontSize": FONT_SIZE+60,
                    "goto": 0
                }
            }
        ]
    }
]
