import pygame
import copy

class SpriteSheet(object):

    def __init__(self, filename, screen, frames, pos_x, pos_y, active=True):
        
        # Get the sheet into memory
        sheet = pygame.image.load(filename).convert()

        self.images = []
        frame_width, frame_height = sheet.get_size()
        frame_width /= frames
        for image_number in range(frames):
            rect = pygame.Rect(image_number * frame_width, 0, frame_width, frame_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)
            self.images.append(image)

        self.pos_x = pos_x - image.get_width()/2
        self.pos_y = pos_y - image.get_height()/2
        self.screen = screen
        self.frame_counter = 0
        self.end_frame = frames
        self.active = active

    def set_pos(self, position):
        self.pos_x = position[0] - self.images[-1].get_width()/2
        self.pos_y = position[1] - self.images[-1].get_height()/2

    def update(self):
        if self.active:
            self.next()
        self.draw()

    def next(self):
        if self.frame_counter == self.end_frame - 1:
            self.frame_counter = 0
        else:
            self.frame_counter += 1

    def set_frame(self, frame_index):
        if frame_index >= 0 and frame_index <= self.end_frame:
            self.frame_counter = frame_index
        else:
            raise Exception("Tried to set to frame number outside frame count: " + frame_index)

    def draw(self):
        self.screen.blit(self.images[self.frame_counter], (self.pos_x, self.pos_y))


class ZoomableSpriteSheet(object):

    def __init__(self, filename, screen, frames, smallest_size, zoom_rate_pixels_per_frame, pos_x, pos_y, active=True):
        
        self.sprite_sheets = [SpriteSheet(filename, screen, frames, pos_x, pos_y, active)]

        # These are squares so we get one dimension.
        width = self.sprite_sheets[0].images[0].get_width()
        diff = width - smallest_size
        number_of_spritesheets_needed = diff / zoom_rate_pixels_per_frame

        # Make sure it can be done.
        if number_of_spritesheets_needed - int(number_of_spritesheets_needed) != 0:
            raise Exception("Number of frames must be divisible by the difference between the minimum and maximum. Number: " + str(number_of_spritesheets_needed))

        # Iterate through and create some scaled images.
        for index_ss in range(int(number_of_spritesheets_needed) - 1):

            # Create a new sheet.
            ss = SpriteSheet(filename, screen, frames, pos_x, pos_y, active)
            
            # Iterate through each of the images and shrink them.
            for index, image in enumerate(ss.images):
                ss.images[index] = pygame.transform.smoothscale(image, (image.get_width() - (zoom_rate_pixels_per_frame * (index_ss + 1)), image.get_height() - (zoom_rate_pixels_per_frame) * (index_ss + 1)))
            
            # Adjust the positions.
            ss.pos_x = pos_x - ss.images[0].get_width()/2
            ss.pos_y = pos_y - ss.images[0].get_height()/2

            # Add this sheet to the sheets list.
            self.sprite_sheets.append(ss)

        # This function sets everything to defaults.
        self.cleanup()

        # Need to swap around the frames for smallest to largest.
        self.sprite_sheets.reverse()

        # Default the first image to not active.
        self.sprite_sheets[0].active = False

    def set_pos(self, position):
        for spritesheet in self.sprite_sheets:
            spritesheet.set_pos(position)


    def update(self):
        # Logic for zooming.
        if self.zoom_counter != len(self.sprite_sheets) - 1 and self.zoom_in:
            self.zoom_counter += 1
        if self.zoom_counter != 0 and self.zoom_out:
            self.zoom_counter -= 1

        # Logic for if active or not.
        if self.zoom_counter != 0:
            self.sprite_sheets[self.zoom_counter].active = True

        # Set the frame on this sheet the the frame from the last sheet.
        self.sprite_sheets[self.zoom_counter].frame_counter = self.previous_frame

        # Run update on this sprite sheet.
        self.sprite_sheets[self.zoom_counter].update()

        # Store this frame for the next update.
        self.previous_frame = self.sprite_sheets[self.zoom_counter].frame_counter

    def cleanup(self):
        self.previous_frame = 0
        self.zoom_counter = 0
        self.zoom_in = False
        self.zoom_out = True






if __name__ == "__main__":
    
    # For testing this class.
    screen = pygame.display.set_mode((640,480))
    ss = ZoomableSpriteSheet("../assets/img/buttons/test_spritesheet.png", screen, 6, 156, 5, 256, 256)
    # ss = SpriteSheet("../assets/img/buttons/test_spritesheet.png", screen, 6, 128, 128)
    clock = pygame.time.Clock()
    FPS = 15

    while True:
        clock.tick(FPS)
        ss.update()
      
        pygame.display.flip()

        # Clear the screen.
        screen.fill((0,0,0,100))
        

        


