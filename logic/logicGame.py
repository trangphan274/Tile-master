import random
from logic.typeGame import BlockType, GameConfigType

GRID_COLS = 8
GRID_ROWS = 6
BLOCK_SIZE = 50
LAYER_X_OFFSET = BLOCK_SIZE // 4  # Lệch ngang giữa các lớp
LAYER_Y_OFFSET = BLOCK_SIZE // 2  # Lệch dọc giữa các lớp

def dict_to_game_config(config_dict):
    return GameConfigType(
        level_num=config_dict["level"],
        random_blocks=config_dict.get("randomBlocks", False),
        animals=["bird.png", "dog.png", "tree.png", "turtle.png"],  # Truyền danh sách động vật vào đây
        blocks=[],  # Danh sách blocks trống
        pattern=config_dict["pattern"]
    )

def calculate_blocks_from_pattern(pattern):
    total_blocks = 0
    for layer in pattern:  # Duyệt qua từng lớp
        for row in layer:  # Duyệt qua từng hàng
            total_blocks += len(row)  # Đếm tổng số ô trong mỗi hàng
    return total_blocks

class Game:
    def __init__(self, game_config: GameConfigType):
        # Cập nhật số lượng block theo số block của pattern
        self.num_blocks = calculate_blocks_from_pattern(game_config.pattern)
        self.current_score = 0
        self.game_over = False
        self.blocks = game_config.blocks
        self.selected_blocks = []
        self.max_selected = 5  # Giới hạn số block chọn
        self.level_num = game_config.level_num
        self.block_types = game_config.animals
        self.build_game(game_config)

    def is_win(self):
        return all(block.status == 0 for block in self.blocks)

    def build_game(self, game_config: GameConfigType):
        blocks = self.generate_blocks(game_config)
        if len(blocks) < calculate_blocks_from_pattern(game_config.pattern):
            raise ValueError("Not enough blocks generated for the given pattern.")
        self.blocks = self.arrange_blocks(blocks, game_config)


    def generate_blocks(self, game_config: GameConfigType):
        total_blocks = calculate_blocks_from_pattern(game_config.pattern)
        blocks = []
        block_types = game_config.animals

        for i in range(total_blocks):  # Tạo block theo số lượng từ pattern
            blocks.append(BlockType(
                block_id=i,
                x=0,  # Gán tạm, sẽ được cập nhật trong arrange_blocks
                y=0,
                level=0,  # Gán tạm
                type_=None,  # Sẽ được gán từ pattern
                status=1
            ))
        return blocks

    def arrange_blocks(self, blocks, game_config: GameConfigType):
        arranged_blocks = []
        PADDING = 30 # khoảng cách giữa các block
        layer_height = BLOCK_SIZE //2  # Khoảng cách giữa các lớp

        for level in range(len(game_config.pattern)):  # Duyệt qua từng lớp
            pattern_layer = game_config.pattern[level]
            for row_idx, row in enumerate(pattern_layer):
                for col_idx, cell in enumerate(row):
                    if cell:  # Nếu ô này có block
                        if not blocks:  # Nếu hết block, báo lỗi
                            raise ValueError("Số lượng block không đủ cho pattern!")
                        block = blocks.pop()

                        # Tính toán vị trí trong lưới
                        block.x = col_idx * (BLOCK_SIZE + PADDING)+ + level * LAYER_X_OFFSET
                        block.y = row_idx * (BLOCK_SIZE + PADDING) + + level * LAYER_Y_OFFSET
                        block.level = level  # Lớp hiện tại
                        block.type_ = cell  # Loại block lấy từ pattern

                        arranged_blocks.append(block)
        return arranged_blocks

    def is_block_visible(self, block):
        for other in self.blocks:
            if (other.block_id != block.block_id and
                other.level > block.level and
                other.x == block.x and
                other.y == block.y and 
                other.status == 1):
                return False
        return True

    def update_visibility(self):
        for block in self.blocks:
            if block.status == 1:
                block.visible = self.is_block_visible(block)

    def select_block(self, block):
        if block not in self.selected_blocks:
            self.selected_blocks.append(block)
            block.status = 0
            print(f"Block {block.block_id} selected and moved to the slot.")
            self.update_visibility()

        self.match_blocks_in_slot()

        if len(self.selected_blocks) >= self.max_selected:
            self.game_over = True
            print("Game Over! Slot is full.")

        self.check_win_condition()

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



    def check_win_condition(self):
        if all(block.status == 0 for block in self.blocks):
            print("Congratulations! You cleared all blocks.")
            self.game_over = True

    def game_status(self):
        if self.game_over:
            return f"Game Over! Final Score: {self.current_score}"
        else:
            return f"Current Score: {self.current_score}, Selected Blocks: {len(self.selected_blocks)}"

    def reset_game(self, game_config: GameConfigType):
        self.blocks = []
        self.current_score = 0
        self.game_over = False
        self.selected_blocks = []
        self.build_game(game_config)