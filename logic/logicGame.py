import random
from logic.typeGame import BlockType, GameConfigType

GRID_COLS = 8
GRID_ROWS = 6
BLOCK_SIZE = 50

def dict_to_game_config(config_dict):
    return GameConfigType(
        level_num=config_dict["level"],
        random_blocks=config_dict.get("randomBlocks", False),
        animals=["bird.png", "dog.png", "tree.png", "turtle.png"],  # Truyền danh sách động vật vào đây
        blocks=[],  # Danh sách blocks trống
        pattern=config_dict["pattern"]
    )

class Game:
    def __init__(self, game_config: GameConfigType):
        self.num_blocks = game_config.level_num * 3  # Mỗi level có 3 block
        self.current_score = 0
        self.game_over = False
        self.blocks = game_config.blocks
        self.selected_blocks = []
        self.max_selected = 5  # Giới hạn số block chọn
        self.level_num = game_config.level_num
        self.block_types = game_config.animals
        self.build_game(game_config)

    def is_win(self):
        return all(block.is_removed for block in self.blocks)

    def build_game(self, game_config: GameConfigType):
        blocks = self.generate_blocks(game_config)
        arranged_blocks = self.arrange_blocks(blocks, game_config)
        self.blocks = arranged_blocks

    def generate_blocks(self, game_config: GameConfigType):
        block_types = game_config.animals
        if not block_types:  # Kiểm tra nếu block_types trống
            raise ValueError("block_types không thể trống")
        blocks = []
        
        for i in range(self.num_blocks // 3):
            block_type = random.choice(block_types)  # Chọn ngẫu nhiên từ block_types
            for _ in range(3):
                blocks.append(BlockType(
                    block_id=len(blocks),
                    x=0,  # Gán tạm
                    y=0,
                    level=0,  # Gán tạm
                    type_=block_type,  # Loại block
                    status=1
                ))
        return blocks


    def arrange_blocks(self, blocks, game_config: GameConfigType):
        grid_positions = set()
        arranged_blocks = []
        
        for level in range(self.level_num):
            level_block_num = self.num_blocks // self.level_num
            for _ in range(level_block_num):
                while True:
                    x = random.randint(0, GRID_COLS - 1) * BLOCK_SIZE
                    y = random.randint(0, GRID_ROWS - 1) * BLOCK_SIZE
                    if (x, y) not in grid_positions:
                        grid_positions.add((x, y))
                        block = blocks.pop()
                        block.x, block.y = x, y
                        block.level = level
                        arranged_blocks.append(block)
                        break
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
            if block.type not in count:
                count[block.type] = 0
            count[block.type] += 1

        for block_type, num in count.items():
            if num >= 3:
                print(f"Matched 3 blocks of type {block_type}!")
                blocks_to_remove = [block for block in self.selected_blocks if block.type == block_type][:3]
                for block in blocks_to_remove:
                    self.selected_blocks.remove(block)
                    block.is_removed = True
                self.current_score += 3
                break

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
