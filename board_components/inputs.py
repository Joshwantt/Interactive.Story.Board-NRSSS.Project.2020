from gpiozero import Button
from multiprocessing import Process
from time import time
import pygame
import settings


class InputController(object):


    button_one_pressed = False
    button_two_pressed = False
    escape_pressed = False
    
    def __init__(self, debug=False, debounce_time=1):
        self.debug = debug
        if not debug:
            # The buttons on the board.
            self.button_one = KidsButton(settings.BUTTON_ONE, debounce_time=debounce_time)
            self.button_two = KidsButton(settings.BUTTON_TWO, debounce_time=debounce_time)
            self.shutdown_button = Button(settings.SHUTDOWN)
            self.shutdown_button.when_pressed = settings.shutdown
        else:
            self.button_one = pygame.K_a
            self.button_two = pygame.K_b
            self.escape = pygame.K_ESCAPE

    def update(self, events):
        self.check_pressed(events)

    def check_pressed(self, events):
        if not self.debug:
            self.button_one_pressed = self.button_one.debounced_is_pressed()
            self.button_two_pressed = self.button_two.debounced_is_pressed()
        else:
            # Reset keys.
            self.button_one_pressed = False
            self.button_two_pressed = False
            self.escape_pressed = False

            # Check if a keydown event has been triggered.
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == self.button_one:
                         self.button_one_pressed = True
                    if event.key == self.button_two:
                         self.button_two_pressed = True
                    if event.key == self.escape:
                         self.escape_pressed = True
                     

    def kill_all(self):
        if not self.debug:
            self.button_one.kill_all()
            self.button_two.kill_all()
                    



class KidsButton(Button):

    def __init__(self, pin, debounce_time=1):
        super(KidsButton, self).__init__(pin)
        self.debounce_time = debounce_time
        self.terminate = False
        self.process = Process(target=self.debounce_timer)
    
    def debounced_is_pressed(self):
        if self.is_pressed and not self.process.is_alive():
            self.process = Process(target=self.debounce_timer)
            self.process.start()
            return True
        return False
    
    def debounce_timer(self):
        """
        This function will wait for a specified amount of time before allowing the button to be pressed again.
        """
        start = time()
        while time() - start < self.debounce_time:
            if self.terminate:
                self.process.terminate()
        self.process.terminate()

    def kill_all(self):
        """
        This function will kill any running threads.
        """
        self.process.terminate()
