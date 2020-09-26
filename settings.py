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
MESSAGE_LOCATION = (960, 960)
MESSAGE_TIMER = 5.0
INITIAL_CYCLE_TIMER = 4
CYCLE_BUTTON_TIMER = INITIAL_CYCLE_TIMER
# Set channels.
pygame.mixer.set_num_channels(3)
NARRATION = pygame.mixer.Channel(0)
SELECTED_EFFECTS = pygame.mixer.Channel(1)
SOUND_EFFECTS = pygame.mixer.Channel(2)
TRANSITION_SOUND = pygame.mixer.Sound("assets/bell.wav")
SELECTED_SOUND = pygame.mixer.Sound("assets/selected.wav")
READBACK_TRANSISION = False
REABBACK_BUTTON_FREEZE = False
PAGE_TURN = "auto"
IN_GAME = False

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
    print(SYSTEM)
    if SYSTEM == "Linux":
        #call("clear", shell=True)
        #call("sudo shutdown -h now", shell=True)
        #this code is commented for dev reasons. Comment this code to gain access back into the device.
        pygame.quit()
    else:
        pygame.quit()



menu_narrative = [

    { #0
        "title": "Welcome to the adventure!",
        "not_random": "Yes",
        "buttons": [
            {
                "image": "assets/img/buttons/start.png",
                "frames" : 4,
                "location": [650, 530],
                "text": "Start",
                "sound_hover" : "start.wav",
                "effects": {
                    "not_random": "Yes",
                    "manager": "having this key will swap the manager. This value doesnt matter."
                }
            },
            {
                "image": "assets/img/buttons/options.png",
                "frames" : 4,
                "location": [1270, 530],
                "text": "Options",
                "sound_hover" : "options.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 1
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
                "location": [450, 530],
                "text": "Switches",
                "sound_hover" : "switches.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 2

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 530],
                "text": "Speed",
                "sound_hover" : "speed.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 3
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [1470, 530],
                "text": "Story",
                "sound_hover" : "story.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 4
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [450, 700],
                "text": "Text",
                "sound_hover" : "text.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 8
                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 700],
                "text": "Turn Page",
                "sound_hover" : "turnpage.wav",
                "effects": {
                    "not_random": "Yes",
                    "goto": 9
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1470, 700],
                "text": "Shutdown",
                "sound_hover" : "shutdown.wav",
                "effects": {
                    "not_random": "Yes",
                    "plain_function": shutdown
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
                "sound_hover" : "oneswitch.wav",
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
                "sound_hover" : "twoswitch.wav",
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
                "sound_hover" : "slower.wav",
                "effects": {
                    "not_random": "Yes",
                    "speedChange": 1,
                    "goto": 0

                }
            },
            {
                "image": "assets/img/buttons/twobuttons.png",
                "frames" : 4,
                "location": [960, 620],
                "text": "Reset("+str(INITIAL_CYCLE_TIMER)+")",
                "sound_hover" : "reset.wav",
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
                "sound_hover" : "faster.wav",
                "effects": {
                    "not_random": "Yes",
                    "speedChange": -0.5,
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
                "sound_hover" : "beginning.wav",
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
                "sound_hover" : "middle.wav",
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
                "sound_hover" : "end.wav",
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
                "sound_hover" : "optionone.wav",
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
                "sound_hover" : "optiontwo.wav",
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
                "sound_hover" : "optionone.wav",
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
                "sound_hover" : "optiontwo.wav",
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
                "sound_hover" : "optionone.wav",
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
                "sound_hover" : "optiontwo.wav",
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
                "sound_hover" : "default.wav",
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
                "sound_hover" : "bigger.wav",
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
                "sound_hover" : "biggest.wav",
                "effects": {
                    "not_random": "Yes",
                    "fontSize": FONT_SIZE+60,
                    "goto": 0
                }
            }
        ]
    },
    { #8
        "title": "Page Turn",
        "not_random": "Yes",
        "buttons": [
            {
                "image": "assets/img/buttons/start.png",
                "frames" : 4,
                "location": [300, 620],
                "text": "1-Switch",
                "sound_hover" : "oneswitch.wav",
                "effects": {
                    "not_random": "Yes",
                    "pageTurn": "default",
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/options.png",
                "frames" : 4,
                "location": [760, 620],
                "text": "2-Switch",
                "sound_hover" : "twoswitch.wav",
                "effects": {
                    "not_random": "Yes",
                    "pageTurn": "both",
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1200, 620],
                "text": "Auto 10s",
                "sound_hover" : "auto.wav",
                "effects": {
                    "not_random": "Yes",
                    "pageTurn": "auto",
                    "goto": 0
                }
            },
            {
                "image": "assets/img/buttons/shutdown.png",
                "frames" : 4,
                "location": [1620, 620],
                "text": "No Page",
                "sound_hover" : "nopage.wav",
                "effects": {
                    "not_random": "Yes",
                    "pageTurn": "off",
                    "goto": 0
                }
            }
        ]
    }
]
