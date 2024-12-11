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
        blocks = self.generate_blocks(game_config)
        arranged_blocks = self.arrange_blocks(blocks)
        self.blocks = arranged_blocks

    def generate_blocks(self, game_config: GameConfigType):
        total_blocks = game_config.level_block_num
        block_types = game_config.animals
        blocks = []
        
        # Chia thành các bộ 3 (hoặc cặp nếu cần)
        for i in range(total_blocks // 3):
            block_type = random.choice(block_types)
            for _ in range(3):  # Tạo 3 block giống nhau
                blocks.append(BlockType(
                    block_id=len(blocks),
                    x=0,  # Gán tạm, sẽ cập nhật sau
                    y=0,
                    level=0,  # Gán tạm
                    type_=block_type,
                    status=1
                ))
        return blocks

    def arrange_blocks(self, blocks):
        random.shuffle(blocks)  # Trộn block để tăng tính ngẫu nhiên
        arranged_blocks = []
        for level in range(1, GRID_ROWS + 1):
            for block in blocks:
                block.level = level
                block.x = random.randint(0, GRID_COLS - 1) * BLOCK_SIZE
                block.y = random.randint(0, GRID_ROWS - 1) * BLOCK_SIZE
                arranged_blocks.append(block)
        return arranged_blocks

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
