import arcade
from game.master import Master

# Import constants
from game.constants import SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE

# Create window
Master(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)

# Run program
arcade.run()