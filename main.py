import pygame
import sys

from UI.menu_UI import menu_UI
from UI.levels_UI import draw_blocks_with_images,draw_bottom_bar,handle_block_click,center_grid,draw_help_buttons
from logic.levelsGame import easy_game_config, middle_game_config, hard_game_config
from logic.logicGame import Game, dict_to_game_config


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (245, 220, 185) # màu nền


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile master")

running = True
grid_offset = None 
game = None
def on_mode_selected(mode):
    global grid_offset
    print(f"Selected mode: {mode}")
    if mode == "easy":
        game_config = easy_game_config
    elif mode == "medium":
        game_config = middle_game_config
    else:
        game_config = hard_game_config

    global game
    game = Game(game_config=dict_to_game_config(game_config))
    print(f"Game initialized with {len(game.blocks)} blocks.")
    grid_offset=center_grid(game)
   

menu_UI(screen,on_mode_selected)

# khởi tạo
if game is None:
    print("Game configuration not loaded correctly.")
    pygame.quit()
    sys.exit()

# Main game loop
running = True

while running:
    screen.fill(WHITE)

    
    draw_blocks_with_images(screen, game,grid_offset)
    draw_bottom_bar(screen,game)
    draw_help_buttons(screen, game)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_block_click(screen,event.pos,game,grid_offset)

    pygame.display.update()

pygame.quit()