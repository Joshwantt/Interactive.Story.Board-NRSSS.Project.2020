import pygame
import settings
from os.path import join


class GUIButton(object):
    def __init__(self, screen, pos, text, sound_hover=None):
        self.selected = False
        self.screen = screen
        self.fontsize = settings.FONT_SIZE
        
        
        # Only get this sound if it has a sound passed in.
        if sound_hover:
            self.hover_sound = pygame.mixer.Sound(join("assets", "SoundHover", sound_hover))
        else:
            self.hover_sound = None

        # Variable for the first frame of being selected.
        self.previously_selected = False

        self.text = text
        self.pos = pos
        
        # Create a font. At this stage, its nothing at 25 pt.
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

    def set_pos(self, position):
        self.pos = position

    def update(self):
        self.draw()
        self.font = pygame.font.Font(None, self.fontsize)
        
        if self.selected == True:
            # If size of button is less than maximum allowed size, increase size
            # Only increase font if selected
            if self.fontsize < settings.FONT_SIZE + settings.BUTTON_MAX_ZOOM:
                self.fontsize = self.fontsize + settings.BUTTON_ZOOM_RATE
        else:
            # If size of button is more than minimum allowed size, decrease size
            # Only decrease font if not selected
            if self.fontsize > settings.FONT_SIZE:
                self.fontsize = self.fontsize - int(settings.BUTTON_ZOOM_RATE + (settings.BUTTON_ZOOM_RATE/2))

        # Check if this is the first frame and if so, play the hover sound.
        if not self.previously_selected and self.selected:
            self.play_hover_sound()
        self.previously_selected = self.selected

    def draw(self):           
        # Draw label.
        if self.selected == True:
            text = self.font.render(self.text, True, settings.SELECTED_COLOUR)
        else:
            text = self.font.render(self.text, True, settings.LABEL_COLOUR)
        text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + text.get_height()/2))
        self.screen.blit(text, text_rect)

    def cleanup(self):
        self.selected = False

    def play_hover_sound(self):
        if self.hover_sound:
            settings.SELECTED_EFFECTS.play(self.hover_sound)


