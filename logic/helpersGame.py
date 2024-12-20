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


def triple_break(game: Game,screen):

    remaining_blocks = [block for block in game.blocks if not block.is_removed]
    block_groups = {}
    
    # Nhóm các block theo loại
    for block in remaining_blocks:
        if block.type_ not in block_groups:
            block_groups[block.type_] = []
        block_groups[block.type_].append(block)

    selected_group = None
    for group in block_groups.values():
        if len(group) >= 3:
            selected_group = group[:3]
            break
    
    if selected_group:
       
        for block in selected_group:
            block.is_removed = True
            block.status = 0
            game.update_visibility()
    game.check_win_condition(screen)

        
       

        
    
