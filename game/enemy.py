from arcade import Sprite
import arcade
from random import randint

# Import constants
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_LEFT_FILENAMES, ENEMY_RIGHT_FILENAMES,\
    ENEMY_DOWN_FILENAMES, ENEMY_UP_FILENAMES

class Enemy(Sprite):
    '''Holds the information needed to update and display the enemy.
    
    Attributes:
        filename (String): The path to the sprite
        center_x (Int): The center x-coordinate of the Sprite
        center_y (Int): The center y-coordinate of the Sprite
        image_x (Int): The starting x-coordinate of the sprite
        image_y (Int): The starting y-coordinate of the sprite
        width (Int): The width of the sprite
        height (Int): The height of the sprite
        velocity (Int): The speed and direction of the enemy

        animation_filenames (List): The paths to the current sprites in use
        animation_index (Int): The index of the current sprite in use
        keep_walking (Int): The number of updates the enemy should keep walking in its current direction
        next_sprite (Int): The updates to skip before updating the sprite
        killed (Bool): Whether or not the enemy has been killed
    '''
    def __init__(self):
        super().__init__()
        self.filename = None
        self.center_x = None
        self.center_y = None
        self.image_x = None
        self.image_y = None
        self.width = 20
        self.height = 30
        self.velocity = [0, 0]

        self.animation_filenames = []
        self.animation_index = 0
        self.keep_walking = 0
        self.next_sprite = 0
        self.killed = False

        self._prepare()
    
    def _prepare(self):
        '''Prepares the Enemy Sprite.'''
        # Get the starting velocity options
        options = [(randint(0, SCREEN_WIDTH - 10), 15), (randint(0, SCREEN_WIDTH - 10), SCREEN_HEIGHT - 15), (10, randint(0, SCREEN_WIDTH - 10)), (SCREEN_WIDTH - 10, randint(0, SCREEN_WIDTH - 10))]
        index = randint(0, 3)

        # Load the starting sprite
        self.filename = ENEMY_DOWN_FILENAMES[0]
        arcade.load_texture(self.filename)

        # Set the enemy's starting location
        self.set_position(options[index][0], options[index][1])
        self.image_x = self.center_x - 10
        self.image_y = self.center_y - 15
    
    def on_update(self, delta_time: float = 1 / 60):
        '''Updates the Sprite.'''
        # If the keep_walking countdown has ended...
        if self.keep_walking == 0:   
            break_loop = False
            velocity_options = [-1, 1]

            # While a valid velocity has not been found, keep generating a new velocity
            while not break_loop:
                options = [[0, velocity_options[randint(0, 1)]], [velocity_options[randint(0, 1)], 0]]
                index = randint(0, 1)

                if self.center_x - 7 + options[index][0] > 0 and self.center_x + 7 + options[index][0] < SCREEN_WIDTH:
                    break_loop = True
                else:
                    break_loop = False
                    continue

                if self.center_y - 13 + options[index][1] > 0 and self.center_y + 13 + options[index][1] < SCREEN_HEIGHT:
                    break_loop = True
                else:
                    break_loop = False
                    continue
            
            # Set the new velocity
            self.velocity = options[index]

            # Get the new enemy sprites and reset the sprite cooldown
            if self.velocity[0] == -1:
                self.animation_filenames = ENEMY_LEFT_FILENAMES
                self.next_sprite = 10
                sprite_change = True
            
            elif self.velocity[0] == 1:
                self.animation_filenames = ENEMY_RIGHT_FILENAMES
                self.next_sprite = 10
                sprite_change = True
            
            elif self.velocity[1] == 1:
                self.animation_filenames = ENEMY_UP_FILENAMES
                self.next_sprite = 10
                sprite_change = True
            
            elif self.velocity[1] == -1:
                self.animation_filenames = ENEMY_DOWN_FILENAMES
                self.next_sprite = 10
                sprite_change = True
            
            else:
                self.animation_filenames = ENEMY_DOWN_FILENAMES
                self.next_sprite = 10
            
            # Reset the keep_walking cooldown
            self.keep_walking = randint(14, SCREEN_WIDTH)
        
        # Otherwise, decrease the keep_walking cooldown
        else:
            self.keep_walking -= 1
        
        # If the sprite cooldown has ended, load the next sprite and reset the cooldown. Otherwise, decrease the cooldown
        if self.next_sprite == 0:
            self.filename = self.animation_filenames[self.animation_index]
            self.texture = arcade.load_texture(self.filename)
            self.next_sprite = 10
            sprite_change = True
        else:
            self.next_sprite -= 1
            sprite_change = False

        # If the sprite has been change, increase the animation index
        if sprite_change:
            self.animation_index = (self.animation_index + 1) % 4

        # If the enemy has hit an edge, don't move in that direction and end the keep_walking cooldown
        if self.center_x + 7 + self.velocity[0] > SCREEN_WIDTH or self.center_x - 7 + self.velocity[0] < 0:
            change_x = False
            self.keep_walking = 0
        else:
            change_x = True
        
        if self.center_y + 13 + self.velocity[1] > SCREEN_HEIGHT or self.center_y - 13 + self.velocity[1] < 0:
            change_y = False
            self.keep_walking = 0
        else:
            change_y = True

        # Set the enemy position  
        if change_x and not change_y:
            self.set_position(self.center_x + self.velocity[0], self.center_y)
        
        elif not change_x and change_y:
            self.set_position(self.center_x, self.center_y + self.velocity[1])
        
        else:
            self.set_position(self.center_x + self.velocity[0], self.center_y + self.velocity[1])
    
    def is_hit(self, is_hit: bool):
        '''Checks if the enemy has been hit.'''
        # If the enemy has been hit, set killed to True
        if is_hit:
            self.killed = True