from typing import List, Callable

# Định nghĩa BlockType
class BlockType:
    def __init__(self, block_id: int, x: int, y: int, level: int, type_: str, status: int):
        self.id = block_id  # ID của khối
        self.x = x          # Vị trí X
        self.y = y          # Vị trí Y
        self.level = level  # Cấp độ của khối
        self.type = type_   # Loại của khối
        self.status = status  # Trạng thái của khối
        self.higher_than_blocks = []  # Các khối nằm trên khối này
        self.lower_than_blocks = []  # Các khối nằm dưới khối này

# Định nghĩa ChessBoardUnitType
class ChessBoardUnitType:
    def __init__(self):
        self.blocks: List[BlockType] = []  # Danh sách các khối trong ô này

# Định nghĩa GameConfigType
class GameConfigType:
    def __init__(self, slot_num: int, compose_num: int, type_num: int, level_block_num: int, 
        border_step: int, level_num: int, random_blocks: List[int], animals: List[str], blocks: List[BlockType] = None):
        self.slot_num = slot_num  # Số lượng khe
        self.compose_num = compose_num  # Số lượng khối cần hợp thành
        self.type_num = type_num  # Số loại động vật
        self.level_block_num = level_block_num  # Số khối trên mỗi cấp
        self.border_step = border_step  # Bước thu hẹp biên
        self.level_num = level_num  # Số cấp độ
        self.random_blocks = random_blocks  # Số lượng khối ngẫu nhiên
        self.animals = animals  # Mảng các loại động vật
        self.blocks = blocks or []  # Danh sách các blocks, mặc định là rỗng

# Định nghĩa SkillType
class SkillType:
    def __init__(self, name: str, desc: str, icon: str, action: Callable):
        self.name = name  # Tên kỹ năng
        self.desc = desc  # Mô tả kỹ năng
        self.icon = icon  # Biểu tượng kỹ năng
        self.action = action  # Hành động của kỹ năng (hàm)
class BlockType:
    def __init__(self, block_id, x, y, level, type_, status):
        self.block_id = block_id
        self.x = x
        self.y = y
        self.level = level
        self.type = type_  # Loại hình (ví dụ: 'turtle.png', 'dog.png')
        self.status = status
        self.visible = True
        self.is_removed = False  # Trạng thái đã xóa
