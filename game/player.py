from arcade import Sprite
import arcade

# Import constants
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_LEFT_FILENAMES, PLAYER_RIGHT_FILENAMES,\
    PLAYER_UP_FILENAMES, PLAYER_DOWN_FILENAMES, PLAYER_ATTACK_LEFT_FILENAMES, PLAYER_ATTACK_RIGHT_FILENAMES,\
    PLAYER_ATTACK_UP_FILENAMES, PLAYER_ATTACK_DOWN_FILENAMES

class Player(Sprite):
    '''Holds the player's current score as well as other information needed to
    update and display the player character.

    Attributes:
        filename (String): The path to the sprite
        center_x (Int): The center x-coordinate of the Sprite
        center_y (Int): The center y-coordinate of the Sprite
        image_x (Int): The starting x-coordinate of the sprite
        image_y (Int): The starting y-coordinate of the sprite
        width (Int): The width of the sprite
        height (Int): The height of the sprite

        attack_filenames (List): The paths to the sprites for the attack animation
        animation_filenames (List): The paths to the current sprites in use
        animation_index (Int): The index of the current sprite in use
        attack (Bool): Whether or not the player is attacking
        next_sprite (Int): The updates to skip before updating the sprite

        key_input (String): The current key input
        mouse_click (Bool): Whether or not the mouse has been clicked

        score (Int): The player's current score
        direction (String): The current direction the player is facing
        health (Int): The player's current health
        immunity (Int): The number of updates the player will be invincible for
        game_over (Bool): Whether or not the player has been killed
    '''
    def __init__(self):
        super().__init__()
        self.filename = None
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.image_x = SCREEN_WIDTH / 2 - 10
        self.image_y = SCREEN_HEIGHT / 2 - 10
        self.width = 20
        self.height = 30

        self.attack_filenames = []
        self.animation_filenames = PLAYER_DOWN_FILENAMES
        self.animation_index = 0
        self.attack = False
        self.next_sprite = 0

        self.key_input = None
        self.mouse_click = False

        self.score = 0
        self.direction = 'down'
        self.health = 10
        self.immunity = 0
        self.game_over = False
    
    def on_update(self, delta_time: float = 1 / 60):
        '''Updates the Sprite.'''
        # If the player has run out of health, set game_over to True
        if self.health == 0:
            self.game_over = True
        
        # If the player has clicked the mouse and is not already attacking...
        if self.mouse_click and not self.attack:
            # Set attack to True
            self.attack = True

            # Change the sprites to match the player's current direction and reset the sprite countdown and the animation index.
            if self.direction == 'left':
                if self.attack_filenames != PLAYER_ATTACK_LEFT_FILENAMES:
                    self.attack_filenames = PLAYER_ATTACK_LEFT_FILENAMES
                    self.animation_index = 0
                    self.next_sprite = 15
                    sprite_change = True

            elif self.direction == 'right':
                if self.attack_filenames != PLAYER_ATTACK_RIGHT_FILENAMES:
                    self.attack_filenames = PLAYER_ATTACK_RIGHT_FILENAMES
                    self.animation_index = 0
                    self.next_sprite = 15
                    sprite_change = True

            elif self.direction == 'up':
                if self.attack_filenames != PLAYER_ATTACK_UP_FILENAMES:
                    self.attack_filenames = PLAYER_ATTACK_UP_FILENAMES
                    self.animation_index = 0
                    self.next_sprite = 15
                    sprite_change = True
            
            elif self.direction == 'down':
                if self.attack_filenames != PLAYER_ATTACK_DOWN_FILENAMES:
                    self.attack_filenames = PLAYER_ATTACK_DOWN_FILENAMES
                    self.animation_index = 0
                    self.next_sprite = 15
                    sprite_change = True
            
            # Set mouse_click to False
            self.mouse_click = False

        # If the player is not attacking and has not clicked the mouse...
        elif not self.attack:
            # Determine which key has been pressed (if a valid key has been pressed), set the new position, change the sprites and
            # direction, and reset the index and sprite countdown if necessary
            if self.key_input == 'a':
                if self.center_x - 25 > 0:
                    self.set_position(self.center_x - 15, self.center_y)
                if self.animation_filenames != PLAYER_LEFT_FILENAMES:
                    self.animation_filenames = PLAYER_LEFT_FILENAMES
                    self.direction = 'left'
                    self.animation_index = 0
                    self.next_sprite = 10
                    sprite_change = True

            elif self.key_input == 'd':
                if self.center_x + 25 < SCREEN_WIDTH:
                    self.set_position(self.center_x + 15, self.center_y)
                if self.animation_filenames != PLAYER_RIGHT_FILENAMES:
                    self.animation_filenames = PLAYER_RIGHT_FILENAMES
                    self.direction = 'right'
                    self.animation_index
                    self.next_sprite = 10
                    sprite_change = True

            elif self.key_input == 'w':
                if self.center_y + 40 < SCREEN_HEIGHT:
                    self.set_position(self.center_x, self.center_y + 25)
                if self.animation_filenames != PLAYER_UP_FILENAMES:
                    self.animation_filenames = PLAYER_UP_FILENAMES
                    self.direction = 'up'
                    self.animation_index = 0
                    self.next_sprite = 10
                    sprite_change = True
            
            elif self.key_input == 's':
                if self.center_y - 40 > 0:
                    self.set_position(self.center_x, self.center_y - 25)
                if self.animation_filenames != PLAYER_DOWN_FILENAMES:
                    self.animation_filenames = PLAYER_DOWN_FILENAMES
                    self.direction = 'down'
                    self.animation_index = 0
                    self.next_sprite = 10
                    sprite_change = True
            
            # Set key_input to None
            self.key_input = None
        
        # If the attack has ended, reset the sprites to normal
        if self.attack == True and self.animation_index == 2:
            self.attack = False
            self.animation_index = 0
            self.next_sprite = 10
            sprite_change = True
            self.filename = self.animation_filenames[self.animation_index]
        
        # If the attack is still in progress...
        elif self.attack == True and self.animation_index < 2:
            # Check if the sprite cooldown has ended. If it has, change the sprite and reset the cooldown. If not, decrease the cooldown
            if self.next_sprite == 0:
                sprite_change = True
                self.next_sprite = 15
                self.filename = self.attack_filenames[self.animation_index]
            else:
                self.next_sprite -= 1
                sprite_change = False

        # Otherwise...
        else:
            # If the sprite cooldown has ended, change the sprite and reset the cooldown. Otherwise, decrease the cooldown
            if self.next_sprite == 0:
                self.filename = self.animation_filenames[self.animation_index]
                self.next_sprite = 10
                sprite_change = True
            else:
                self.next_sprite -= 1
                sprite_change = False
        
        # If the player is still invincible, decrease the countdown
        if self.immunity > 0:
            self.immunity -= 1
        
        # If the sprite has been changed, load the new sprite and increase the animation index
        if sprite_change:
            self.texture = arcade.load_texture(self.filename)
            self.animation_index = (self.animation_index + 1) % 4

    def is_hit(self, is_hit: bool):
        '''Checks if the player has been hit and updates the player's health and immunity accordingly.'''
        # If the player has been hit and the immunity countdown has ended, decrease the player's health and reset the
        # immunity countdown
        if is_hit and self.immunity == 0:
            self.health -= 1
            self.immunity = 100