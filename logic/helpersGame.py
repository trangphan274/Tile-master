import random
from logic.logicGame import Game

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
def triple_break(game: Game):
    # Tìm các nhóm 3 block cùng loại
    from collections import Counter

    remaining_blocks = [block for block in game.blocks if not block.is_removed]
    block_groups = {}
    
    for block in remaining_blocks:
        if block.type_ not in block_groups:
            block_groups[block.type_] = []
        block_groups[block.type_].append(block)
    
    # Duyệt qua các loại block và bể 3 viên cùng loại
    for block_type, blocks in block_groups.items():
        if len(blocks) >= 3:
            # Chọn 3 viên để bể
            for i in range(3):
                blocks[i].is_removed = True

    game.update_visibility()
    
