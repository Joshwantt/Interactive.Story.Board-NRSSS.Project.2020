import pygame
from board_components.inputs import InputController
from board_components.outputs import Fan, VibeMat, Rotors
from game_objects.gui_button import GUIButton
import settings
from threading import Timer
from time import sleep


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
        self.swap_manager = False
        self.mode = "easy"
        self.button_cycle_timer = 2.0
        self.active_button_cycle_timer = None
        self.active_scene_transition_timer = None
        self.message = ""
        self.scene_active = False
        self.narrative_played = False
        self.scene_wind_down = False

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
        if self.mode == "easy":
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
            self.draw_text_lines(self.narrative[self.scene_number]["title"], self.screen.get_width()/2, self.screen.get_height()/3)

            
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

            for button in self.narrative[self.scene_number]["buttons"]:
                self.buttons.append(button["preload_button"])

            # Set button one to selected.
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
            # Here is where we handle when to transition scenes.
            self.destroy_cycle_timer()
            if not pygame.mixer.get_busy() and (not self.active_scene_transition_timer or not self.active_scene_transition_timer.is_alive()):
                settings.SOUND_EFFECTS.play(settings.TRANSITION_SOUND)
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

        if self.mode == "easy":
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


class GameManager(Manager):

    def __init__(self, json, screen, input_controller):
        super(GameManager, self).__init__(json, screen, input_controller)
        self.outputs = {
            "fan" : Fan(settings.FAN, settings.FAN_PULSE_DURATION, settings.FAN_PULSE_INTERVAL, settings.FAN_PULSE_TOTAL),
            "rotors" : Rotors(settings.ROTORS, settings.ROTORS_PULSE_DURATION, settings.ROTORS_PULSE_INTERVAL, settings.ROTORS_PULSE_TOTAL),
            "vibe_mat" : VibeMat(settings.VIBE_MAT, settings.VIBE_MAT_PULSE_DURATION, settings.VIBE_MAT_PULSE_INTERVAL, settings.VIBE_MAT_PULSE_TOTAL)
        }
       

    def check_pressed(self):
        if self.input_controller.button_one_pressed:
            self.destroy_cycle_timer()
            self.buttons[self.selected_button].selected = True
            self.process_button_effects()

        if self.input_controller.button_two_pressed:
            self.cycle_button()


    def process_button_effects(self):

        # We have a special key called effects and this function will process it.
        effects = self.narrative[self.scene_number]["buttons"][self.selected_button].get("effects")

        # If there is no effects key, just go to the next scene.
        if effects:

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
        if "plain_function" in effects:
            effects["plain_function"]()
        if "goto" in effects:
            self.set_scene_index(effects["goto"])


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
            else:
                for button in self.menu_manager.buttons:
                    button.cleanup()
                self.menu_manager.buttons[0].selected = True
                self.menu_manager.auto_button_cycle(start=True)
            self.in_menu = not self.in_menu
