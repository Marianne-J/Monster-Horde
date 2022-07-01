import arcade
from random import randint
from game.enemy import Enemy
from game.player import Player

# Import constants
from game.constants import BACKGROUND_FILENAME, SCREEN_HEIGHT, SCREEN_WIDTH

class Master(arcade.Window):
    '''Handles drawing to the window, managing updates to the Sprites, and adding
    and removing Sprites.

    Attributes:
        enemies (SpriteList): Contains all of the Enemy Sprites
        player (Player): The Player Sprite
        background (String): Path to the background of the game
        add_enemy_cooldown (Int): The number of updates to skip adding an enemy
        game_over (Bool): Whether or not the game is over
        end_score (Int): The player's final score
    '''
    def __init__(self, width, height, title):
        '''The class constructor.'''
        super().__init__(width, height, title)
        self.enemies = arcade.SpriteList()
        self.player = Player()
        self.background = None
        self.add_enemy_cooldown = 100
        self.game_over = False
        self.end_score = 0

        self._prepare()
    
    def on_draw(self):
        '''Draws objects to the window.'''
        # Clear the window
        self.clear()

        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw()

        # If the game is not over, draw the player. Otherwise, draw the game over text
        if not self.game_over:
            self.player.draw()
        else:
            arcade.draw_text('GAME OVER!', SCREEN_WIDTH / 2 - 210, SCREEN_HEIGHT / 2 + 40, arcade.color.RED, 40, 400, bold = True, align = 'center')
            arcade.draw_text('TOTAL SCORE: ' + str(self.end_score), SCREEN_WIDTH / 2 - 210, SCREEN_HEIGHT / 2 - 40, arcade.color.RED, 18, 400, bold = True, align = 'center')
        
        # If the game is not over, draw the score text and the health text
        if not self.game_over:
            score = self.player.score
            health = self.player.health
            arcade.draw_text('SCORE: ' + str(score), 5, SCREEN_HEIGHT - 30, arcade.color.BLACK, 16, 10, bold = True)
            arcade.draw_text('HEALTH: ' + str(health), 5, SCREEN_HEIGHT - 50, arcade.color.BLACK, 16, 10, bold = True)

    def update(self, delta_time: float):
        '''Updates the state of play and the Sprites.'''
        
        # If there are less than eight enemies on the screen and the cooldown has ended, add an enemy and reset the cooldown.
        # Otherwise, decrease the cooldown
        if len(self.enemies.sprite_list) < 8 and self.add_enemy_cooldown == 0:
            self.enemies.append(Enemy())
            self.add_enemy_cooldown = 100
        else:
            self.add_enemy_cooldown -= 1
        
        # If the game is not over, update the Player Sprite
        if not self.game_over:
            self.player.on_update()

        for enemy in self.enemies:
            # Update the Enemy Sprite
            enemy.on_update()

            # If the game is not over...
            if not self.game_over:
                # Check if the player has collided with this enemy
                is_hit = arcade.check_for_collision(self.player, enemy)

                # Check if the enemy was attacked. If so, set the player hit variable to False
                enemy_hit = False
                if is_hit:
                    if self.player.direction == 'left' and enemy.center_x + 7 < self.player.center_x and self.player.attack:
                        enemy_hit = True
                        is_hit = False
                    elif self.player.direction == 'right' and enemy.center_x - 7 > self.player.center_x  and self.player.attack:
                        enemy_hit = True
                        is_hit = False
                    elif self.player.direction == 'up' and enemy.center_y - 13 < self.player.center_y and self.player.attack:
                        enemy_hit = True
                        is_hit = False
                    elif self.player.direction == 'down' and enemy.center_y + 13 > self.player.center_y and self.player.attack:
                        enemy_hit = True
                        is_hit = False

                # Call the Sprite methods to deal with collisions
                enemy.is_hit(enemy_hit) 
                self.player.is_hit(is_hit)

                # If the enemy has been killed, remove it from the SpriteList and add to the player's score
                if enemy.killed:
                    self.enemies.remove(enemy)
                    self.player.score += 50

                # If the player is dead, get the final score, remove the Player Sprite, and set game_over to True
                if self.player.game_over:
                    self.end_score = self.player.score
                    self.player = None
                    self.game_over = True     

    def on_key_press(self, symbol: int, modifiers: int):
        '''Determines what key was pressed and saves it to the Player Sprite.'''
        # If the game is not over, save the key pressed to the Player Sprite
        if not self.game_over:
            if symbol == arcade.key.A:
                self.player.key_input = 'a'
            elif symbol == arcade.key.D:
                self.player.key_input = 'd'
            elif symbol == arcade.key.W:
                self.player.key_input = 'w'
            elif symbol == arcade.key.S:
                self.player.key_input = 's'

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        '''Tells the Player Sprite if there was a mouse click.'''
        # If the game is not over and the player is not already attacking, tell the Player Sprite there was a mouse click
        if not self.game_over:
            if not self.player.attack:
                self.player.mouse_click = True

    def _prepare(self):
        '''Prepares the game.'''
        # Load the background image
        self.background = arcade.load_texture(BACKGROUND_FILENAME)
        
        # Add the starting amount of enemies
        for _ in range(randint(3, 6)):
            self.enemies.append(Enemy())