import random
from logic.typeGame import BlockType, GameConfigType

GRID_COLS = 8
GRID_ROWS = 6
BLOCK_SIZE = 50

def dict_to_game_config(config_dict):
    return GameConfigType(
        slot_num=config_dict["slotNum"],
        compose_num=config_dict["composeNum"],
        type_num=config_dict["typeNum"],
        level_block_num=config_dict["levelBlockNum"],
        border_step=config_dict["borderStep"],
        level_num=config_dict["levelNum"],
        random_blocks=config_dict["randomBlocks"],
        animals=config_dict["animals"],
        blocks=[]  # Khởi tạo danh sách blocks rỗng
    )

class Game:
    def __init__(self, game_config: GameConfigType):
        self.num_blocks = game_config.level_block_num
        
        self.current_score = 0
        self.game_over = False
        self.blocks = game_config.blocks
        self.selected_blocks = []
        self.max_selected = game_config.slot_num
        self.level_num = game_config.level_num
        self.block_types = game_config.animals
        self.build_game(game_config)
    def is_win(self):
        # Kiểm tra nếu tất cả các block đã được chọn
        return all(block.is_removed for block in self.blocks)

    def build_game(self, game_config: GameConfigType):
        for level in range(1, self.level_num + 1):
            for _ in range(game_config.level_block_num // self.level_num):
                block_type = random.choice(self.block_types)
                x = random.randint(0, GRID_COLS - 1) * BLOCK_SIZE
                y = random.randint(0, GRID_ROWS - 1) * BLOCK_SIZE
                block = BlockType(
                    block_id=len(self.blocks),
                    x=x,
                    y=y,
                    level=level,
                    type_=block_type,
                    status=1
                )
                self.blocks.append(block)

    def is_block_visible(self, block):
        for other in self.blocks:
            if (
                other.block_id != block.block_id and 
                other.level > block.level and
                other.x == block.x and
                other.y == block.y and 
                other.status == 1
            ):
                return False
        return True

    def update_visibility(self):
        for block in self.blocks:
            if block.status == 1:
                block.visible = self.is_block_visible(block)

    def select_block(self, block):
        if block not in self.selected_blocks:
            self.selected_blocks.append(block)
            block.status = 0  # Đánh dấu block đã được chọn
            print(f"Block {block.block_id} selected and moved to the slot.")
            self.update_visibility()

        # Kiểm tra trong thanh nếu có 3 hình giống nhau
        self.match_blocks_in_slot()

        # Nếu thanh đầy, báo game over
        if len(self.selected_blocks) >= self.max_selected:
            self.game_over = True
            print("Game Over! Slot is full.")

        self.check_win_condition()
    def match_blocks_in_slot(self):
        """Xóa 3 block giống nhau trong thanh nếu có"""
        count = {}
        # Đếm số lượng từng loại block trong thanh
        for block in self.selected_blocks:
            if block.type not in count:
                count[block.type] = 0
            count[block.type] += 1

        # Tìm loại block có đủ 3 hình
        for block_type, num in count.items():
            if num >= 3:
                print(f"Matched 3 blocks of type {block_type}!")
                # Xóa 3 block đầu tiên thuộc loại này
                blocks_to_remove = [block for block in self.selected_blocks if block.type == block_type][:3]
                for block in blocks_to_remove:
                    self.selected_blocks.remove(block)  # Xóa khỏi thanh
                    block.is_removed = True  # Đánh dấu là đã xóa
                self.current_score += 3  # Tăng điểm
                break  # Thoát vòng lặp sau khi xóa 3 hình

    def check_win_condition(self):
        if all(block.status == 0 for block in self.blocks):
            print("Congratulations! You cleared all blocks.")
            self.game_over = True

    def game_status(self):
        if self.game_over:
            return f"Game Over! Final Score: {self.current_score}"
        else:
            return f"Current Score: {self.current_score}, Selected Blocks: {len(self.selected_blocks)}"

    def reset_game(self):
        self.blocks = []
        self.current_score = 0
        self.game_over = False
        self.selected_blocks = []
        self.build_game()

if __name__ == "__main__":
    example_config_dict = {
        "slotNum": 7,
        "composeNum": 3,
        "typeNum": 12,
        "levelBlockNum": 24,
        "borderStep": 1,
        "levelNum": 6,
        "randomBlocks": [8, 8],
        "animals": ["turtle.png", "dog.png", "tree.png", "bird.png"]
    }

    game_config = dict_to_game_config(example_config_dict)
    game = Game(game_config=game_config)
    print(game.game_status())
