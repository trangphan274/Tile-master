import pygame
import sys

from UI.main_menu_UI import menu_UI
from UI.levels_UI import draw_blocks_with_images,draw_bottom_bar,handle_block_click,center_grid,draw_help_buttons,draw_game_menu_button
from logic.levelsGame import easy_game_config, middle_game_config, hard_game_config
from logic.logicGame import Game, dict_to_game_config
from UI.game_menu_UI import draw_game_menu_ui

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (245, 220, 185) # màu nền


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile master")

running = True
grid_offset = None 
game = None
paused =False

def on_mode_selected(mode):
    global grid_offset, game_config
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





running = True
while running:
    
    if paused:
        screen.fill(WHITE)
        draw_blocks_with_images(screen, game, grid_offset)
        draw_bottom_bar(screen, game)
        draw_help_buttons(screen, game)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  
        screen.blit(overlay, (0, 0))
        action = draw_game_menu_ui(screen)
        

        if action == "resume":
            paused = False  
        elif action == "replay":
            game.reset_game(game_config)  
            paused = False
        elif action == "back_home":
            paused =False
            game=None
            grid_offset=None
            menu_UI(screen,on_mode_selected)  
        elif action == "quit":
            paused = False

    else:
        screen.fill(WHITE)
        draw_blocks_with_images(screen, game,grid_offset)
        draw_bottom_bar(screen,game)
        draw_help_buttons(screen, game)
        draw_game_menu_button(screen,game)
        action = draw_game_menu_button(screen, game)
        if action == "menu_pressed":
            paused = True

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not paused:
                handle_block_click(screen,event.pos,game,grid_offset)

    pygame.display.update()

pygame.quit()