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

        # Dự đoán trạng thái sau khi phá nhóm
        simulated_groups = block_groups.copy()
        simulated_groups[largest_group[0].type_] = simulated_groups[largest_group[0].type_][3:]
        simulated_groups = {k: v for k, v in simulated_groups.items() if len(v) > 0}

        # Tính nhóm lớn nhất kế tiếp trong trạng thái mô phỏng
        next_largest_group = max(simulated_groups.values(), key=len, default=[])

        # So sánh nhóm tiếp theo với nhóm hiện tại
        if len(next_largest_group) >= 3 or len(simulated_groups) > 1:
            # Phá nhóm hiện tại
            for block in blocks_to_remove:
                block.is_removed = True
                block.status = 0
        else:
            print("avoid deadlock")

    game.check_win_condition(screen)






        
       

        
    
