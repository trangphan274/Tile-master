import pygame
BLOCKS_PIC ={
    "alien":   "Resources/block_icon/alien.jpg",
    "cheese":    "Resources/block_icon/cheese.png", 
    "coffee":    "Resources/block_icon/coffee.png",
    "cream":    "Resources/block_icon/cream.png",
    "bat":    "Resources/block_icon/bat.png ",
    "fork":    "Resources/block_icon/fork.png",
    "hat":    "Resources/block_icon/hat.png ",
    "jam":    "Resources/block_icon/jam.png ",
    "juice":    "Resources/block_icon/juice.png ",
    "pancake":    "Resources/block_icon/pancake.png",
    "shovel":    "Resources/block_icon/shovel.png",
    "sock":    "Resources/block_icon/sock.png ",
    "strawberry":    "Resources/block_icon/strawberry.png ",
    "tree":    "Resources/block_icon/tree.png ",
    "turtle":   "Resources/block_icon/turtle.png",
    "water":    "Resources/block_icon/water.png "           
        }


HELPER_PIC={
    "shuffle":"Resources/Helper/shuffle.png",
    "triple":"Resources/Helper/magic_eye.png"
}

GAME_MENU_PIC={
    "resume":"Resources/game board/resume.png ",
    "replay":"Resources/game board/replay.png",
    "quit":"Resources/game board/quit.png ",
    "back_home":"Resources/game board/back_home.png",
    "game_menu":"Resources/game board/game_menu.png",
    "menu_board":"Resources/game board/menu_board.png"
}
RESULT_PIC={
    "win_board":"Resources/game board/win_board.png",
    "win_cat":"Resources/game board/win_cat.png",
    "lose_board":"Resources/game board/lose_board.png",
    "lose_cat":"Resources/game board/lose_cat.png"
}



BLOCKS_PIC_LOADED = {}

for key, path in BLOCKS_PIC.items():
    try:
        BLOCKS_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")

HELPER_PIC_LOADED={}

for key, path in HELPER_PIC.items():
    try:
        HELPER_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")

GAME_MENU_PIC_LOADED= {}

for key, path in GAME_MENU_PIC.items():
    try:
        GAME_MENU_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")

RESULT_PIC_LOADED ={}
for key, path in RESULT_PIC.items():
    try:
        RESULT_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")




# print(f"Loaded images: {BLOCKS_PIC_LOADED.keys()}")


print(RESULT_PIC_LOADED)