from typing import List, Callable

# Định nghĩa BlockType
class BlockType:
    def __init__(self, block_id: int, x: int, y: int, level: int, type_: str, status: int):
        self.block_id  = block_id  # ID của khối
        self.x = x          # Vị trí X
        self.y = y          # Vị trí Y
        self.level = level  # Cấp độ của khối
        self.type = type_   # Loại của khối
        self.status = status  # Trạng thái của khối
        self.higher_than_blocks = []  # Các khối nằm trên khối này
        self.lower_than_blocks = []  # Các khối nằm dưới khối này
        self.visible = True
        self.is_removed = False  # Trạng thái đã xóa

class GameConfigType:
    def __init__(self, level_num, random_blocks, block_pic, blocks, pattern, layer_offsets=None):
        self.level_num = level_num  
        self.random_blocks = random_blocks
        self.block_pic = block_pic 
        self.blocks = blocks
        self.pattern = pattern  
        # Nếu không có layer_offsets, tạo mặc định với các x_offset và y_offset
        self.layer_offsets = layer_offsets if layer_offsets is not None else [{"x_offset": 0, "y_offset": 0} for _ in range(len(pattern))]



class SkillType:
    def __init__(self, name: str, desc: str, icon: str, action: Callable):
        self.name = name  # Tên kỹ năng
        self.desc = desc  # Mô tả kỹ năng
        self.icon = icon  # Biểu tượng kỹ năng
        self.action = action  # Hành động của kỹ năng (hàm)
