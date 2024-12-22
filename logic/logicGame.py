import random
import pygame 
from logic.typeGame import BlockType, GameConfigType
from Resources.assets import BLOCKS_PIC
from UI.game_over_UI import draw_game_over_screen
import time

GRID_COLS = 8
GRID_ROWS = 6
BLOCK_SIZE = 50


def dict_to_game_config(config_dict):
    num_layers = len(config_dict["pattern"])    
    if "layer_offsets" not in config_dict:
        config_dict["layer_offsets"] = [{"x_offset": 0, "y_offset": 0}] * num_layers

    
    
    # Tạo đối tượng GameConfigType
    return GameConfigType(
        level_num=config_dict["level"],
        
        block_pic=list(BLOCKS_PIC.keys()),
        blocks=[],  
        pattern=config_dict["pattern"],
        layer_offsets=config_dict["layer_offsets"],  
    )

def calculate_blocks_from_pattern(pattern):
    
    return sum(sum(1 for cell in row if cell) for layer in pattern for row in layer)
class Game:
    def __init__(self, game_config: GameConfigType):
        
        self.num_blocks = calculate_blocks_from_pattern(game_config.pattern)
        self.current_score = 0
        self.game_over = False
        self.blocks = game_config.blocks
        self.selected_blocks = []
        self.max_selected = 7  
        self.level_num = game_config.level_num
        self.block_types = game_config.block_pic
        self.layer_offsets = game_config.layer_offsets
        self.remaining_blocks = self.num_blocks
        # Lưu x_offset và y_offset từ layer_offsets
        self.x_offset = [layer["x_offset"] for layer in game_config.layer_offsets]
        self.y_offset = [layer["y_offset"] for layer in game_config.layer_offsets]
        
        self.build_game(game_config)


    
    def build_game(self, game_config: GameConfigType):
        blocks = self.generate_blocks(game_config)
        if len(blocks) < calculate_blocks_from_pattern(game_config.pattern):
            raise ValueError("Not enough blocks generated for the given pattern.")
        self.arranged_blocks = self.arrange_blocks(blocks, game_config)


    def generate_blocks(self, game_config: GameConfigType):
        total_blocks = calculate_blocks_from_pattern(game_config.pattern)
        blocks = []
        block_types = game_config.block_pic

        if not block_types:
            raise ValueError("Danh sách hình block không được rỗng!")

        for i in range(total_blocks):
            block = BlockType(
                block_id=i,
                x=0,  # Gán tạm, sẽ cập nhật sau
                y=0,
                level=0,  # Gán tạm
                type_=block_types[i % len(block_types)],
                status=1
            )
            blocks.append(block)
        
        return blocks



    
#/////////////////////////////////////////////////////////////////////

    def arrange_blocks(self, blocks, game_config: GameConfigType):
        arranged_blocks = []
        #print(f"Số lượng block trước khi arrange: {len(blocks)}")  # Debug: In số lượng block

        for level, pattern_layer in enumerate(game_config.pattern):
            total_needed_blocks = sum(sum(1 for cell in row if cell) for row in pattern_layer)
            
            if len(blocks) < total_needed_blocks:
                raise ValueError(f"Số lượng block không đủ cho pattern! Cần {total_needed_blocks} block, nhưng chỉ có {len(blocks)} block.")

            x_offset = game_config.layer_offsets[level]["x_offset"]
            y_offset = game_config.layer_offsets[level]["y_offset"]
            padding = game_config.layer_offsets[level].get("padding")
            for row_idx, row in enumerate(pattern_layer):
                for col_idx, cell in enumerate(row):
                    if cell:  # Nếu ô này có block
                        if not blocks:  # Nếu hết block, báo lỗi
                            raise ValueError("Số lượng block không đủ cho pattern!")
                        block = blocks.pop()

                        block.x = col_idx * (BLOCK_SIZE + padding) + x_offset
                        block.y = row_idx * (BLOCK_SIZE + padding) + y_offset

                        block.level = level  # Lớp hiện tại
                        block.type_ = cell  # Loại block lấy từ pattern

                        arranged_blocks.append(block)
        self.blocks = arranged_blocks

        return arranged_blocks


 
    def is_block_interactable(self, block):
        for other in self.blocks:
            if other.block_id != block.block_id and other.level > block.level and other.status == 1:  # Kiểm tra trạng thái
                if pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE).colliderect(
                    pygame.Rect(other.x, other.y, BLOCK_SIZE, BLOCK_SIZE)
                ):
                    return False  # Block bị cản, không thể tương tác
        return True  # Block có thể tương tác

    def update_visibility(self):
    # After selecting or removing blocks, ensure visibility is updated for all blocks
        for block in self.blocks:
            if block.status !=0:
                # Update the visibility status for the block if it's not covered
                block.visible = self.is_block_visible(block)
                block.interactable = self.is_block_interactable(block)

    # Check if a block is visible (not obscured by others)
    def is_block_visible(self, block):
        for other in self.blocks:
            if other.block_id != block.block_id and other.level > block.level and other.status == 1:  # Kiểm tra trạng thái
                if pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE).colliderect(
                    pygame.Rect(other.x, other.y, BLOCK_SIZE, BLOCK_SIZE)
                ):
                    return False  # Block bị che
        return True  # Block không bị che

    
    def match_blocks_in_slot(self):
        for block in self.selected_blocks:
            # Kiểm tra có đủ 3 block cùng loại không
            matching_blocks = [b for b in self.selected_blocks if b.type_ == block.type_]
            if len(matching_blocks) >= 3:
                print(f"Matched 3 blocks of type {block.type_}!")
                # Xóa 3 block giống nhau
                blocks_to_remove = matching_blocks[:3]
                for block in blocks_to_remove:
                    self.selected_blocks.remove(block)
                    block.is_removed = True
                self.current_score += 3
                break  # Ngừng kiểm tra sau khi đã bể 1 loại block

    def select_block(self, block,screen):
        if self.game_over:
            return
        if block not in self.selected_blocks:
            self.selected_blocks.append(block)
            block.status = 0  # Đánh dấu block đã bị xóa
            print(f"Block {block.block_id} selected and moved to the slot.")

            self.update_visibility()  
            self.match_blocks_in_slot()  

            if len(self.selected_blocks) >= self.max_selected:
                self.game_over = True
                print("Game Over! Slot is full.")
                draw_game_over_screen(screen, False)

            self.check_win_condition(screen)

   

    def is_win(self):
        return all(block.status == 0 for block in self.blocks)

    def check_win_condition(self,screen):
        if all(block.status == 0 for block in self.blocks):
            if not self.game_over:
                print("Congratulations! You cleared all blocks.")
                self.game_over = True                
                for block in self.blocks:
                    block.is_removed =True
                draw_game_over_screen(screen, True)

    def reset_game(self, game_config: GameConfigType):
        if isinstance(game_config, dict):  
            game_config = dict_to_game_config(game_config)
        self.blocks = []
        self.game_over = False
        self.selected_blocks = []
        self.build_game(game_config)