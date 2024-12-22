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

    # Nếu nhóm lớn nhất có ít nhất 3 viên
    if len(largest_group) >= 3:
        # Chỉ lấy 3 viên đầu tiên để phá
        blocks_to_remove = largest_group[:3]

        # Tính toán và dự đoán xem có nên phá nhóm này hay không
        next_largest_group = max(
            [group for group in block_groups.values() if group != largest_group], 
            key=len, 
            default=[]
        )

        # So sánh nhóm lớn tiếp theo với nhóm hiện tại để tránh bế tắc
        if len(next_largest_group) >= 3:
            # Nếu nhóm tiếp theo cũng lớn và có thể sẽ giúp sau này, thì cứ phá nhóm hiện tại
            for block in blocks_to_remove:
                block.is_removed = True
                block.status = 0
        else:
            # Nếu nhóm tiếp theo không có tác dụng nhiều, ta vẫn phá nhóm hiện tại
            for block in blocks_to_remove:
                block.is_removed = True
                block.status = 0

    game.check_win_condition(screen)





        
       

        
    
