import random 
from logic.logicGame import Game
import pygame

def shuffle_blocks(game: Game,screen):
    from UI.levels_UI import center_grid,draw_blocks_with_images
    
    remaining_blocks = [block for block in game.blocks if not block.is_removed]
    block_types = [block.type_ for block in remaining_blocks]

    random.shuffle(block_types)

    # Gán lại blcoktype cho các block còn lại
    for block, new_type in zip(remaining_blocks, block_types):
        block.type_ = new_type

   
    game.update_visibility()
    grid_offset = center_grid(game) 
    draw_blocks_with_images(screen, game, grid_offset)

    print("shuffled successfully!")


def triple_break(game: Game, screen):
    remaining_blocks = [block for block in game.blocks if not block.is_removed]
    block_groups = {}

    # Nhóm các block theo loại
    for block in remaining_blocks:
        block_groups.setdefault(block.type_, []).append(block)

    for group in block_groups.values():
        if len(group) >= 3:
            for block in group[:3]:
                block.is_removed = True
                block.status = 0
            break

    game.check_win_condition(screen)


        
       

        
    
