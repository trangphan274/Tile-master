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
    "back":"Resources/Helper/back.png",
    "triple":"Resources/Helper/magic_eye.png"
}

HELPER_PIC_LOADED={}

for key, path in HELPER_PIC.items():
    try:
        HELPER_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")

BLOCKS_PIC_LOADED = {}

for key, path in BLOCKS_PIC.items():
    try:
        BLOCKS_PIC_LOADED[key] = pygame.image.load(path)
    except pygame.error as e:
        print(f"Error loading image for {key} at {path}: {e}")

# Kiểm tra các hình ảnh đã tải thành công
# print(f"Loaded images: {BLOCKS_PIC_LOADED.keys()}")


