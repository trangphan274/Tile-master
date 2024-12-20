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

    # Lấy x_offset, y_offset từ layer_offsets của từng lớp
    x_offsets = [layer["x_offset"] for layer in config_dict["layer_offsets"]]
    y_offsets = [layer["y_offset"] for layer in config_dict["layer_offsets"]]
    
    # Tạo đối tượng GameConfigType
    return GameConfigType(
        level_num=config_dict["level"],
        random_blocks=config_dict.get("random_blocks", []),
        block_pic=list(BLOCKS_PIC.keys()),
        blocks=[],  
        pattern=config_dict["pattern"],
        layer_offsets=config_dict["layer_offsets"],  #  layer_offsets đã được cập nhật
    )

def calculate_blocks_from_pattern(pattern):
    total_blocks = 0
    for layer in pattern:  
        for row in layer:  
            total_blocks += len(row)  
    return total_blocks

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
        
        # Kiểm tra nếu animals bị rỗng
        if not block_types:
            raise ValueError("Danh sách hình block không được rỗng!")

        for i in range(total_blocks):  # Tạo block theo số lượng từ pattern
            block = BlockType(
                block_id=i,
                x=0,  # Gán tạm, sẽ được cập nhật trong arrange_blocks
                y=0,
                level=0,  # Gán tạm
                type_=block_types[i % len(block_types)],  # Gán kiểu block từ animals
                status=1
            )
            blocks.append(block)
        
        print(f"Số block đã tạo: {len(blocks)}")
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
        count = {}
        for block in self.selected_blocks:
            if block.type_ not in count:
                count[block.type_] = 0
            count[block.type_] += 1

        # Duyệt qua từng loại block
        for block_type, num in count.items():
            if num >= 3:  # Kiểm tra có đủ 3 block cùng loại không
                print(f"Matched 3 blocks of type {block_type}!")
                # Xóa 3 block giống nhau ở bất kỳ vị trí nào trong thanh
                blocks_to_remove = [block for block in self.selected_blocks if block.type_ == block_type][:3]
                for block in blocks_to_remove:
                    self.selected_blocks.remove(block)
                    block.is_removed = True
                self.current_score += 3
                break  # Ngừng việc kiểm tra các loại block khác sau khi đã bể 1 loại

    def select_block(self, block,screen):
        if self.game_over:
            return
        if block not in self.selected_blocks:
            self.selected_blocks.append(block)
            block.status = 0  # Đánh dấu block đã bị xóa
            print(f"Block {block.block_id} selected and moved to the slot.")

            self.update_visibility()  # Đảm bảo cập nhật trạng thái hiển thị ngay sau khi xóa
            self.match_blocks_in_slot()  # Kiểm tra khớp block trong slot

            if len(self.selected_blocks) >= self.max_selected:
                self.game_over = True
                print("Game Over! Slot is full.")
                draw_game_over_screen(screen, False)

        self.check_win_condition(screen)

   

    def is_win(self):
        return all(block.status == 0 for block in self.blocks)

    def check_win_condition(self,screen):
        if all(block.status == 0 for block in self.blocks):
            print("Congratulations! You cleared all blocks.")
            self.game_over = True
            
            for block in self.blocks:
                block.is_removed =True
            pygame.display.flip()
            time.sleep(1)
            draw_game_over_screen(screen, True)

    def reset_game(self, game_config: GameConfigType):
        if isinstance(game_config, dict):  
            game_config = dict_to_game_config(game_config)
        self.blocks = []
        self.current_score = 0
        self.game_over = False
        self.selected_blocks = []
        self.build_game(game_config)