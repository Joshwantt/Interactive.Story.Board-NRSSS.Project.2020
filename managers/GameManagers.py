import json
import pygame
from board_components.inputs import InputController
from board_components.outputs import Fan, VibeMat, Rotors, Custom
from game_objects.gui_button import GUIButton
import settings
from threading import Timer
from time import sleep
import random

class Manager(object):

    def __init__(self, json, screen, input_controller):
        self.narrative = json
        self.input_controller = input_controller
        self.screen = screen
        self.buttons = []
        self.selected_button = 0
        self.scene_number = 0
        # Create a font. At this stage, its nothing at 25 pt.
        self.font = pygame.font.Font(None, settings.FONT_SIZE)
        self.fontMax = pygame.font.Font(None, (settings.FONT_SIZE+settings.BUTTON_MAX_ZOOM))
        self.swap_manager = False
        self.mode = "easy"
        self.button_cycle_timer = settings.CYCLE_BUTTON_TIMER
        self.active_button_cycle_timer = None
        self.active_scene_transition_timer = None
        self.message = ""
        self.scene_active = False
        self.narrative_played = False
        self.scene_wind_down = False
        self.beginning = 1  ##default to all option 1 story
        self.middle = 1     ##if option 2 is needed the variable is set to 2
        self.ending = 1
        self.fontSize = settings.FONT_SIZE
        self.readback = []
        self.randomOptions = [[]]
        self.beginningSkip = False

        self.BegOne = []
        self.BegTwo = []
        self.MidOne = []
        self.MidTwo = []
        self.EndOne = []
        self.EndTwo = []



        for i in self.narrative:
            random.seed()
            a = random.randint(0, 3)
            b = random.randint(4, 6)
            c = random.randint(7, 9)
            self.randomOptions.append([a,b,c])

        for page in range(0, len(self.narrative)):
            if "BeginningOpt1Beg" in self.narrative[page]:
                self.BegOne.append(page-1)
                print(page-1)
            if "BeginningOpt1End" in self.narrative[page]:
                self.BegOne.append(page+1)
                print(page+1)
            if "MiddleOpt1Beg" in self.narrative[page]:
                self.MidOne.append(page-1)
                print(page-1)
            if "MiddleOpt1End" in self.narrative[page]:
                self.MidOne.append(page+1)
                print(page+1)
            if "EndOpt1Beg" in self.narrative[page]:
                self.EndOne.append(page-1)
                print(page-1)
            if "EndOpt1End" in self.narrative[page]:
                self.EndOne.append(page+1)
                print(page+1)
            if "BeginningOpt2Beg" in self.narrative[page]:
                self.BegTwo.append(page-1)
                print(page-1)
            if "BeginningOpt2End" in self.narrative[page]:
                self.BegTwo.append(page+1)
                print(page+1)
            if "MiddleOpt2Beg" in self.narrative[page]:
                self.MidTwo.append(page-1)
                print(page-1)
            if "MiddleOpt2End" in self.narrative[page]:
                self.MidTwo.append(page+1)
                print(page+1)
            if "EndOpt2Beg" in self.narrative[page]:
                self.EndTwo.append(page-1)
                print(page-1)
            if "EndOpt2End" in self.narrative[page]:
                self.EndTwo.append(page+1)
                print(page+1)
            


        # Because the timer thread goes off and does its thing before the game starts, a start bool will be used to set it in update rather than here.
        self.start = True

        # Call this after everything is setup.
        self.setup_buttons()   


    def scene_transisition(self):
        
        # Cleanup some things.
        for button in self.buttons:
            button.cleanup()

        # Clear any messages.
        self.message = ""

        # Setup this scene's buttons.
        self.setup_buttons()

        # If we are in easy mode, need to flag the timers to start in update.
        if self.mode == "easy" or "playback" in self.narrative[self.scene_number]:
            self.start = True

        # Reset narrative
        self.narrative_played = False

        # Finally, set the scene wind down off.
        self.scene_wind_down = False
        self.scene_active = False

    def start_narration(self):
        if "sound_narration" in self.narrative[self.scene_number]:
            settings.NARRATION.play(self.narrative[self.scene_number]["sound_narration"])

    # This function will render the text to the screen. It will also add a new line if the width of the screen is exceeded.
    def render_text(self):
        if "title" in self.narrative[self.scene_number]:
            self.draw_text_lines(self.narrative[self.scene_number]["title"], self.screen.get_width()/2, self.screen.get_height()/5)
            

            
    def draw_text_lines(self, text, x, y):
        first_line = text
        second_line = ""

        text = self.font.render(first_line, True, settings.LABEL_COLOUR)
        text_rect = text.get_rect(center=(x, y))

        while text_rect.width > self.screen.get_width():
            # Get last word and add it to second line.
            split = first_line.rsplit(" ", 1)
            second_line = " " + split[1] + second_line
            first_line = split[0]
            text = self.font.render(
                first_line, True, settings.LABEL_COLOUR)
            text_rect = text.get_rect(center=(x, y))

        if second_line:
            second_text = self.font.render(
                second_line, True, settings.LABEL_COLOUR)
            second_text_rect = second_text.get_rect(center=(x, y + self.font.get_height()))
            self.screen.blit(second_text, second_text_rect)

        self.screen.blit(text, text_rect)

    def setup_buttons(self):
        if "buttons" in self.narrative[self.scene_number]:
            self.buttons.clear()
            if "playback" in self.narrative[self.scene_number]:
                settings.REABBACK_BUTTON_FREEZE = True
                for button in self.narrative[self.scene_number]["buttons"]:
                    self.buttons.append(button["preload_button"])
                for i, button in enumerate(self.buttons):
                    a = self.narrative[self.scene_number]["playback"]
                    if i == 0:
                        button.set_text(self.readback[a][0])
                        button.set_sound_narration(self.readback[a][2])
                    if i == 1:
                        button.set_text(self.readback[a][1])
                        button.set_hover_sound(self.readback[a][3])
                        button.set_sound_selected(self.readback[a][4])

                        #Setting physical feedback
                        effects = self.narrative[self.scene_number]["buttons"][i].get("effects")
                        effects["output"] = self.readback[a][5]
            else:
                settings.REABBACK_BUTTON_FREEZE = False
                enumerateButtons = enumerate(self.narrative[self.scene_number]["buttons"])
                for i, button in enumerateButtons:
                    if "not_random" in self.narrative[self.scene_number]:
                        self.buttons.append(button["preload_button"])
                    else:
                        if (self.randomOptions[self.scene_number][0] == i):
                            self.buttons.append(button["preload_button"])
                            
                        if (self.randomOptions[self.scene_number][1] == i):
                            self.buttons.append(button["preload_button"])
                            
                        if (self.randomOptions[self.scene_number][2] == i):
                            self.buttons.append(button["preload_button"])

            
            # Set button one to selected.if
            self.selected_button = 0

    def render_buttons(self, active=True):
        for button in self.buttons:
            button.update()
        

    def idle_buttons(self):
        for button in self.buttons:
            button.draw()

    def update(self, events):   

        self.render_buttons()
        self.render_text()
        self.render_message()

        if self.scene_wind_down:
            # Here is where we handle when to transition scenes.    ####################################################
            self.destroy_cycle_timer()
            if not pygame.mixer.get_busy() and (not self.active_scene_transition_timer or not self.active_scene_transition_timer.is_alive()):
                #settings.SOUND_EFFECTS.play(settings.TRANSITION_SOUND)    ############ OBSOLETE?
                # Compensates for bell delay
                sleep(.5)
                self.next_scene()
            return


        # Play narrative.
        if not self.narrative_played:
            self.start_narration()
            self.narrative_played = True

        if not self.scene_active and not pygame.mixer.get_busy():
            self.buttons[self.selected_button].selected = True
            self.scene_active = True

        if self.scene_active:
            # Update the inputs.
            self.input_controller.update(events)

            # If we are using in easy mode, we need to ignore the state of the second button.
            if self.mode == "easy":
                self.input_controller.button_two_pressed = False

            # Check for button presses.
            self.check_pressed()

            # Startup the cycle timer.
            if self.start:
                self.auto_button_cycle(start=True)
                self.start = False


    def render_message(self):
        if self.message:
            self.draw_text_lines(self.message, settings.MESSAGE_LOCATION[0], settings.MESSAGE_LOCATION[1])

    def auto_button_cycle(self, start=False):
        if self.active_button_cycle_timer:
            self.active_button_cycle_timer.cancel()

        if (self.mode == "easy") or ("playback" in self.narrative[self.scene_number]):
            if ("playback" in self.narrative[self.scene_number]):
                self.button_cycle_timer = 3
            else:
                self.button_cycle_timer = settings.CYCLE_BUTTON_TIMER

            self.active_button_cycle_timer = Timer(self.button_cycle_timer, self.auto_button_cycle)
            self.active_button_cycle_timer.start()

            # In start mode, it will just set the timer.
            if not start:
                self.cycle_button()

    def destroy_cycle_timer(self):
        if self.active_button_cycle_timer:
            self.active_button_cycle_timer.cancel()

    def check_pressed(self):
        pass

    def cleanup(self):
        self.input_controller.kill_all()

    def next_scene(self):

        ## Scene numbers may need to change if scenes are added for playback feature
        if self.scene_number == self.EndOne[1]:
            self.scene_number = self.EndTwo[1]

        if self.scene_number == self.BegOne[0] and self.beginning == 2:
            self.scene_number = self.EndOne[1]

        if self.scene_number == self.BegOne[1] and self.middle == 2:
            self.scene_number = self.BegTwo[1]

        if self.scene_number == self.MidOne[1] and self.ending == 2:
            self.scene_number = self.MidTwo[1]

        if self.scene_number == self.BegTwo[1] and self.middle == 1:
            self.scene_number = self.MidOne[0]

        if self.scene_number == self.MidTwo[1] and self.ending == 1:
            self.scene_number = self.MidOne[1]

        if settings.PAGE_TURN == "off" and "turn_page" in self.narrative[self.scene_number+1]:
            self.scene_number += 2
        else:
            self.scene_number += 1

        if not self.scene_number >= len(self.narrative):
            self.scene_transisition()

    def previous_scene(self):
        self.scene_number -= 1
        if self.scene_number >= 0:
            self.scene_transisition()
        else:
            raise Exception("Trying to go back to a scene before 0.")

    def set_scene_index(self, number):
        self.scene_number = number
        self.scene_transisition()

    def complete(self):
        if self.scene_number > len(self.narrative) - 1:
            return True

        if self.input_controller.debug and self.input_controller.escape_pressed:
            return True

        return False

    def cycle_button(self):
        self.buttons[self.selected_button].selected = False

        if self.selected_button == len(self.buttons) - 1:
            self.selected_button = 0
        else:
            self.selected_button += 1

        self.buttons[self.selected_button].selected = True

        if "playback" in self.narrative[self.scene_number] and self.selected_button == 2:
            self.scene_wind_down = True

    def check_swap_manager(self):
        if self.swap_manager:
            self.swap_manager = False
            return True
        return False

    def switch_mode(self, mode):

        # Don't do anything if already in this mode
        if mode == self.mode:
            return

        # Change it.
        self.mode = mode
    
    def switch_speed(self, speed):

        # Don't do anything if already in this mode
        if self.button_cycle_timer <= 1:
            return

        # Change it.
        if speed == 3: #if speed is 3 it means that speed is trying to be reset
            self.button_cycle_timer = speed
        else: #else change cycle speed
            self.button_cycle_timer += speed

    def switch_beginning(self, option):
        # Don't do anything if already in this mode
        if option == self.beginning:
            return

        # Change it.
        self.beginning = option

    def switch_middle(self, option):
        # Don't do anything if already in this mode
        if option == self.middle:
            return

        # Change it.
        self.middle = option

    def switch_end(self, option):
        # Don't do anything if already in this mode
        if option == self.ending:
            return

        # Change it.
        self.ending = option

    def switch_font(self, size):
        # Don't do anything if already in this mode
        if size == self.fontSize:
            return

        # Change it.
        self.fontSize = size


class GameManager(Manager):

    def __init__(self, json, screen, input_controller):
        super(GameManager, self).__init__(json, screen, input_controller)
        self.outputs = {
            "fan" : Fan(settings.FAN, settings.FAN_PULSE_DURATION, settings.FAN_PULSE_INTERVAL, settings.FAN_PULSE_TOTAL),
            "rotors" : Rotors(settings.ROTORS, settings.ROTORS_PULSE_DURATION, settings.ROTORS_PULSE_INTERVAL, settings.ROTORS_PULSE_TOTAL),
            "vibe_mat" : VibeMat(settings.VIBE_MAT, settings.VIBE_MAT_PULSE_DURATION, settings.VIBE_MAT_PULSE_INTERVAL, settings.VIBE_MAT_PULSE_TOTAL),
            "custom" : Custom(settings.CUSTOM, settings.CUSTOM_PULSE_DURATION, settings.CUSTOM_PULSE_INTERVAL, settings.CUSTOM_PULSE_TOTAL)
        }
       

    def check_pressed(self):
        if self.input_controller.button_one_pressed and not settings.REABBACK_BUTTON_FREEZE:
            self.destroy_cycle_timer()
            self.buttons[self.selected_button].selected = True
            self.process_button_effects()

        if self.input_controller.button_two_pressed and "turn_page" in self.narrative[self.scene_number] and settings.PAGE_TURN == "both":
            self.destroy_cycle_timer()
            self.buttons[self.selected_button].selected = True
            self.process_button_effects()

        if self.input_controller.button_two_pressed and not settings.REABBACK_BUTTON_FREEZE:
            self.cycle_button()


    def process_button_effects(self):

        # We have a special key called effects and this function will process it.
        if "not_random" in self.narrative[self.scene_number]:
            effects = self.narrative[self.scene_number]["buttons"][self.selected_button].get("effects")
        else:
            effects = self.narrative[self.scene_number]["buttons"][self.selected_button].get("effects")
            effectsRandom = self.narrative[self.scene_number]["buttons"][self.randomOptions[self.scene_number][self.selected_button]].get("effects")
            with open("narrative.json", "r") as f:
                js = json.loads(f.read())
            selectedSound = js[self.scene_number]["buttons"][self.randomOptions[self.scene_number][self.selected_button]].get("effects")
            optionText = js[self.scene_number]["buttons"][self.randomOptions[self.scene_number][self.selected_button]]["text"]

            self.readback.append([self.narrative[self.scene_number]["title"],
                                  " " + optionText,
                                  js[self.scene_number]["sound_narration"],
                                  js[self.scene_number]["buttons"][self.randomOptions[self.scene_number][self.selected_button]]["sound_hover"],
                                  selectedSound["selected_sound"],
                                  selectedSound["output"]])


        # If there is no effects key, just go to the next scene. 
        if effects:
            if "not_random" in effects:
                if "selected_sound" in effects:
                    # Play a default sound if nothing in the field.
                    to_play = effects["selected_sound"] if effects["selected_sound"] else settings.SELECTED_SOUND
                    settings.SOUND_EFFECTS.play(to_play)

                if "sound_narration" in effects:
                    settings.NARRATION.play(effects["sound_narration"])

                if "answer" in effects:
                    self.active_scene_transition_timer = Timer(settings.MESSAGE_TIMER, lambda *args: None)
                    self.active_scene_transition_timer.start()
                    self.message = effects["answer"]

                if "output" in effects:
                    for op in effects["output"]:
                        self.outputs[op].pulse()

                if "restart" in effects:
                    self.scene_number = -1
                    self.readback = []
                    self.swap_manager = True
            else:
                if "selected_sound" in effects:
                    # Play a default sound if nothing in the field.
                    to_play = effectsRandom["selected_sound"] if effectsRandom["selected_sound"] else settings.SELECTED_SOUND
                    settings.SOUND_EFFECTS.play(to_play, 1)
                    

                if "sound_narration" in effectsRandom:
                    settings.NARRATION.play(effectsRandom["sound_narration"])

                if "answer" in effectsRandom:
                    self.active_scene_transition_timer = Timer(settings.MESSAGE_TIMER, lambda *args: None)
                    self.active_scene_transition_timer.start()
                    self.message = effectsRandom["answer"]

                if "output" in effectsRandom:
                    for op in effectsRandom["output"]:
                        self.outputs[op].pulse()

                if "restart" in effectsRandom:
                    self.scene_number = -1
                    self.swap_manager = True



        # After everything is processed, enter scene wind-down mode.
        self.scene_active = False
        self.scene_wind_down = True


class MenuManager(Manager):

    def check_pressed(self):
        if self.input_controller.button_one_pressed:
            self.process_button_effects()

        if self.input_controller.button_two_pressed:
            self.cycle_button()

    def process_button_effects(self):

        # We have a special key called effects and this function will process it.
        effects = self.narrative[self.scene_number]["buttons"][self.selected_button]["effects"]

        if "manager" in effects:
            self.swap_manager = True
        if "mode" in effects:
            self.switch_mode(effects["mode"])
            self.mode = effects["mode"]
        if self.mode == "easy":
            if "speedChange" in effects:
                self.switch_speed(effects["speedChange"])
                self.button_cycle_timer += effects["speedChange"]
                settings.CYCLE_BUTTON_TIMER += effects["speedChange"]
            if "speedReset" in effects:
                self.switch_speed(effects["speedReset"])
                self.button_cycle_timer = effects["speedReset"]
                settings.CYCLE_BUTTON_TIMER = effects["speedChange"]
        if "plain_function" in effects:
            effects["plain_function"]()
        if "goto" in effects:
            self.set_scene_index(effects["goto"])
        if "beginningOption" in effects:
            self.switch_beginning(effects["beginningOption"])
            self.beginning = effects["beginningOption"]
        if "middleOption" in effects:
            self.switch_middle(effects["middleOption"])
            self.middle = effects["middleOption"]
        if "endOption" in effects:
            self.switch_end(effects["endOption"])
            self.ending = effects["endOption"]
        if "fontSize" in effects:
            self.switch_font(effects["fontSize"])
            self.fontSize = effects["fontSize"]
            settings.FONT_SIZE = effects["fontSize"]
        if "pageTurn" in effects:
            settings.PAGE_TURN = effects["pageTurn"]

            
            


class Managers(object):

    def __init__(self, game_manager, menu_manager):
        self.game_manager = game_manager
        self.menu_manager = menu_manager
        self.in_menu = True

        # Settings shared between the managers.
        self.settings = {}

    def update(self, events):

        self.swap_check()

        # Select either the menu or the main game.
        if self.in_menu:
            self.menu_manager.update(events)
        else:
            self.game_manager.update(events)

    def is_complete(self):
        # Check if either manager has registered a complete event and end the loop if so.
        if self.game_manager.complete() or self.menu_manager.complete():
            self.game_manager.destroy_cycle_timer()
            self.menu_manager.destroy_cycle_timer()
            return True
        return False

    def swap_check(self):
        # Check for a toggle in the current running manager.
        if self.menu_manager.check_swap_manager() or self.game_manager.check_swap_manager():
            # Settings are only ever changed from the menu so we update settings when changing from menu to game.
            if self.in_menu:
                self.menu_manager.destroy_cycle_timer()
                self.game_manager.switch_mode(self.menu_manager.mode)
                self.game_manager.switch_speed(self.menu_manager.button_cycle_timer)
                self.game_manager.switch_beginning(self.menu_manager.beginning)
                self.game_manager.switch_middle(self.menu_manager.middle)
                self.game_manager.switch_end(self.menu_manager.ending)
                self.game_manager.switch_font(self.menu_manager.font)

            else:
                for button in self.menu_manager.buttons:
                    button.cleanup()
                self.menu_manager.buttons[0].selected = True
                self.menu_manager.auto_button_cycle(start=True)
            self.in_menu = not self.in_menu
