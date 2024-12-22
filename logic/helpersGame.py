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

#greedy
def triple_break(game: Game, screen):
    remaining_blocks = [block for block in game.blocks if not block.is_removed]
    block_groups = {}

    # Nhóm các block theo loại
    for block in remaining_blocks:
        block_groups.setdefault(block.type_, []).append(block)

    # Tìm nhóm lớn nhất (Greedy)
    largest_group = max(block_groups.values(), key=len, default=[])
    
    # Đảm bảo chỉ phá tối đa 3 viên
    if len(largest_group) >= 3:
        for block in largest_group[:3]:  # Chỉ lấy 3 viên đầu tiên
            block.is_removed = True
            block.status = 0

    game.check_win_condition(screen)



        
       

        
    
