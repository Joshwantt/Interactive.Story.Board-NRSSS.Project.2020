import pygame
import settings
from graphics.spritesheet import ZoomableSpriteSheet
from os.path import join


class GUIButton(object):
    def __init__(self, screen, image_path, pos, text, animation_frames, sound_hover=None):
        self.selected = False
        self.screen = screen
        self.spritesheet = ZoomableSpriteSheet(image_path, screen, animation_frames, settings.BUTTON_MIN_ZOOM, settings.BUTTON_ZOOM_RATE, pos[0], pos[1], active=False)

        # Only get this sound if it has a sound passed in.
        if sound_hover:
            self.hover_sound = pygame.mixer.Sound(join("assets", "SoundHover", sound_hover))
        else:
            self.hover_sound = None

        # Variable for the first frame of being selected.
        self.previously_selected = False

        # Need to get the height of the last frame as it is the largest one.
        largest = len(self.spritesheet.sprite_sheets) - 1
        self.button_centre_y = self.spritesheet.sprite_sheets[largest].images[0].get_height()/2
        
        self.text = text
        self.pos = pos
        
        # Create a font. At this stage, its nothing at 25 pt.
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

    def set_pos(self, position):
        self.pos = position
        self.spritesheet.set_pos(position)

    def update(self):
        # Check for active state of button:
        if self.selected:
            self.spritesheet.zoom_in = True
            self.spritesheet.zoom_out = False
        else:
            self.spritesheet.zoom_in = False
            self.spritesheet.zoom_out = True

        self.spritesheet.update()
        self.draw()

        # Check if this is the first frame and if so, play the hover sound.
        if not self.previously_selected and self.selected:
            self.play_hover_sound()
        self.previously_selected = self.selected

    def draw(self):           
        # Draw label.
        text = self.font.render(self.text, True, settings.LABEL_COLOUR)
        text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + self.button_centre_y + text.get_height()/2))
        self.screen.blit(text, text_rect)

    def cleanup(self):
        self.selected = False
        self.spritesheet.cleanup()

    def play_hover_sound(self):
        if self.hover_sound:
            settings.SELECTED_EFFECTS.play(self.hover_sound)


