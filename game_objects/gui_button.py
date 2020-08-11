import pygame
import settings
from os.path import join


class GUIButton(object):
    def __init__(self, screen, pos, text, effects, sound_narration=None, sound_hover=None, sound_selected=None):
        self.selected = False
        self.screen = screen
        self.fontsize = settings.FONT_SIZE
        self.visible = True
        self.not_played = True
        self.effects = effects
        
        # Only get this sound if it has a sound passed in.
        if sound_hover:
            self.hover_sound = pygame.mixer.Sound(join("assets", "SoundHover", sound_hover))
        else:
            self.hover_sound = None

        if sound_narration:
            self.sound_narration = pygame.mixer.Sound(join("assets", "SoundNarration", sound_narration))
        else:
            self.sound_narration = None

        if sound_selected:
            self.sound_selected = pygame.mixer.Sound(join("assets", "SoundSelected", sound_selected))
        else:
            self.sound_selected = None

        # Variable for the first frame of being selected.
        self.previously_selected = False

        self.text = text
        self.pos = pos
        
        # Create a font. At this stage, its nothing at 25 pt.
        self.font = pygame.font.Font(None, settings.FONT_SIZE)
        self.fontMax = pygame.font.Font(None, settings.FONT_SIZE+settings.BUTTON_MAX_ZOOM)

    def set_invisible(self):
        self.visible = False
        
    def set_sound_narration(self, new_sound_narration):
        self.sound_narration = pygame.mixer.Sound(join("assets", "SoundNarration", new_sound_narration))

    def set_hover_sound(self, new_hover_sound):
        self.hover_sound = pygame.mixer.Sound(join("assets", "SoundHover", new_hover_sound))

    def set_sound_selected(self, new_sound_selected):
        self.sound_selected = pygame.mixer.Sound(join("assets", "SoundSelected", new_sound_selected))
            
    def set_text(self, new_text):
        self.text = new_text

    def set_pos(self, position):
        self.pos = position

    
    
    def update(self):
        
        
        self.draw()
        self.font = pygame.font.Font(None, self.fontsize)

        if self.fontsize < settings.FONT_SIZE:
            self.fontsize = settings.FONT_SIZE
                
        if self.selected == True:
            # If size of button is less than maximum allowed size, increase size
            # Only increase font if selected
            if self.fontsize < settings.FONT_SIZE + settings.BUTTON_MAX_ZOOM:
                self.fontsize = self.fontsize + settings.BUTTON_ZOOM_RATE
        else:
            # If size of button is more than minimum allowed size, decrease size
            # Only decrease font if not selected
            if self.fontsize > settings.FONT_SIZE + settings.BUTTON_MAX_ZOOM:
                self.fontsize = settings.FONT_SIZE
            if self.fontsize > settings.FONT_SIZE:
                self.fontsize = self.fontsize - int(settings.BUTTON_ZOOM_RATE + (settings.BUTTON_ZOOM_RATE/2))

        if "nextPage" in self.effects and self.selected:
            settings.READBACK_TRANSISION = True

        # Check if this is the first frame and if so, play the hover sound.
        if not self.previously_selected and self.selected:
            self.not_played = True
            self.play_hover_sound()
        self.previously_selected = self.selected


    def draw(self):
        if self.visible == True:
            # Draw label.
            first_line = self.text
            second_line = ""
            currentColour = ""
            if self.selected == True:
                text = self.font.render(self.text, True, settings.SELECTED_COLOUR)
                currentColour = settings.SELECTED_COLOUR
            else:
                text = self.font.render(self.text, True, settings.LABEL_COLOUR)
                currentColour = settings.LABEL_COLOUR
            
            textM = self.fontMax.render(self.text, True, settings.LABEL_COLOUR)
            text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + text.get_height()/2))
            textM_rect = textM.get_rect(center=(self.pos[0], self.pos[1] + text.get_height()/2))
            if ((((textM_rect.width/2) + self.pos[0]) > 1910) or (self.pos[0] - textM_rect.width/2 < 10)) and " " in self.text:
                split = first_line.rsplit(" ", 1)
                second_line = " " + split[1] + second_line
                first_line = split[0]
                text = self.font.render(
                    first_line, True, currentColour)
                text_rect = text.get_rect(center=(self.pos[0], self.pos[1] + text.get_height()/2))

            if second_line:
                second_text = self.font.render(
                    second_line, True, currentColour)
                second_text_rect = second_text.get_rect(center=(self.pos[0], self.pos[1] + self.fontMax.get_height()+30))
                self.screen.blit(second_text, second_text_rect)
            
            self.screen.blit(text, text_rect)

    def cleanup(self):
        self.selected = False

    def updateFont(self, size):
        self.fontsize = size

    def play_hover_sound(self):
        if self.hover_sound:
            settings.SELECTED_EFFECTS.play(self.hover_sound)
        if self.sound_narration and self.hover_sound:
            settings.SELECTED_EFFECTS.play(self.sound_narration)
            settings.SELECTED_EFFECTS.queue(self.hover_sound)
        if self.sound_selected:
            settings.SOUND_EFFECTS.play(self.sound_selected)

            



