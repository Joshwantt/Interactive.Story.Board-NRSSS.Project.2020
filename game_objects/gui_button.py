import pygame
import settings
from os.path import join


class GUIButton(object):
    def __init__(self, screen, pos, text, sound_hover=None):
        self.selected = False
        self.screen = screen
        
        
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

        if self.selected == True:
            self.font = pygame.font.Font(None, settings.FONT_SIZE + 35)
        else:
            self.font = pygame.font.Font(None, settings.FONT_SIZE)

        # Check if this is the first frame and if so, play the hover sound.
        if not self.previously_selected and self.selected:
            self.play_hover_sound()
        self.previously_selected = self.selected

    def draw(self):           
        # Draw label.
        text = self.font.render(self.text, True, settings.LABEL_COLOUR)
        text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + text.get_height()/2))
        self.screen.blit(text, text_rect)

    def cleanup(self):
        self.selected = False

    def play_hover_sound(self):
        if self.hover_sound:
            settings.SELECTED_EFFECTS.play(self.hover_sound)


