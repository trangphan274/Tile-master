
import random

# Danh sách động vật
animals = ["Resources/block_icon/alien.jpg", "Resources/block_icon/cheese.png", 
           "Resources/block_icon/coffee.png", "Resources/block_icon/cream.png"]

# Cấu hình Shape và lớp cho từng màn chơi
level_config = {
    1: {
        "pattern": [
            [[1, 1, 1],  # Layer 1
             [1, 1, 1],
             [1, 1, 1]],
            [[1, 1, 1],  # Layer 2
             [1, 1, 1],
             [1, 1, 1]]
        ],
        "time_limit": 60,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0,"padding": 45},
            {"x_offset": 0, "y_offset": 30,"padding": 45}
        ]
    },
    2: {
        "pattern": [
            [[1, 1, 1, 1, 1, 1],  # Layer 1
             [1, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1]],
            [[1, 1, 0, 0, 1, 1],  # Layer 2
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1]]
             
        ],
        "time_limit": 90,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0,"padding": 20},
            {"x_offset": 300, "y_offset": 300,"padding": 20},
           
            
        ]
    },
    3: {
        "pattern": [
            [[1, 1, 1, 1, 1, 1],  # Layer 1
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1]],
            [[1, 1, 1, 1, 1, 1],  # Layer 2
             [1, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 1],
             [1, 0, 1, 1, 0, 1],
             [1, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1]],
            [[0, 0, 1, 1, 0, 0],  # Layer 3
             [0, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 0, 0]]
        ],
        "time_limit": 120,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0,"padding": 20},
            {"x_offset": 10, "y_offset": 20,"padding": 20},
            {"x_offset": 10, "y_offset": 20,"padding": 20},
        ]
    }
}

# Hàm tạo block pool dựa trên tổng số block cần để full đủ bảng
def create_block_pool(total_blocks):
    if not animals:
        raise ValueError("The animals list is empty!")

    block_pool = []
    blocks_per_icon = total_blocks // len(animals)

    for animal in animals:
        count = blocks_per_icon
        while count % 3 != 0:
            count += 3 - (count % 3)  # Điều chỉnh để mỗi loại động vật có bội số của 3
        block_pool.extend([animal] * count)

    # Cắt block pool đúng tổng số block cần
    block_pool = block_pool[:total_blocks]
    random.shuffle(block_pool)
    return block_pool

# Hàm lấp đầy grid theo shape
def fill_layer(shape, block_pool):
    grid = []
    for row in shape:
        grid_row = []
        for cell in row:
            if cell == 1:  # Chỉ lấp block vào ô có shape = 1
                grid_row.append(block_pool.pop())
            else:
                grid_row.append(None)
        grid.append(grid_row)
    return grid

# Hàm tạo pattern cho từng level
def generate_pattern(level):
    config = level_config.get(level)
    if not config:
        raise ValueError(f"No configuration found for level {level}")

    pattern = config["pattern"]
    total_blocks = sum(sum(row.count(1) for row in shape) for shape in pattern)
    while total_blocks % 3 != 0:  # Đảm bảo bội số của 3
        total_blocks += 1

    block_pool = create_block_pool(total_blocks)

    layers = [fill_layer(shape, block_pool) for shape in pattern]
    return layers

# Tạo config game
def create_game_config(level):
    return {
        "level": level,
        "grid_size": (len(level_config[level]["pattern"][0]), len(level_config[level]["pattern"][0][0])),
        "pattern": generate_pattern(level),
        "time_limit": level_config[level]["time_limit"],
        "layer_offsets": level_config[level].get("layer_offsets", [{"x_offset": 0, "y_offset": 0} for _ in range(len(level_config[level]["pattern"]))])
    }

# Ví dụ tạo config cho các màn chơi
easy_game_config = create_game_config(1)
middle_game_config = create_game_config(2)
hard_game_config = create_game_config(3)

