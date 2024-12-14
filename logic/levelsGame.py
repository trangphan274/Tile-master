# import random

# # Danh sách động vật
# animals = ["Resources/block_icon/alien.jpg", "Resources/block_icon/cheese.png", "Resources/block_icon/coffee.png", "Resources/block_icon/cream.png"]

# # Hàm tạo pattern cố định cho mỗi màn
# def generate_fixed_pattern(level):
#     if not animals:
#         raise ValueError("The animals list is empty!")

#     # Xác định kích thước grid theo level
#     grid_size = {
#         1: (3, 3),  # Level 1: 3x3 grid
#         2: (3, 6),  # Level 2: 3x6 grid
#         3: (6, 6)   # Level 3: 6x6 grid
#     }.get(level, (3, 3))  # Default 3x3 grid nếu level không xác định

#     rows, cols = grid_size
#     total_blocks = rows * cols * 2  # Tổng số block cần cho 2 lớp

#     # Đảm bảo tổng số block là bội số của 3
#     while total_blocks % 3 != 0:
#         total_blocks += 1

#     # Tạo block pool
#     block_pool = []
#     blocks_per_icon = total_blocks // len(animals)

#     for animal in animals:
#         # Đảm bảo mỗi loại icon có số lượng chia hết cho 3
#         count = blocks_per_icon
#         while count % 3 != 0:
#             count += 1
#         block_pool.extend([animal] * count)

#     # Nếu block_pool vượt quá total_blocks, cắt bớt
#     block_pool = block_pool[:total_blocks]

#     # Bổ sung các block trống (None) nếu thiếu
#     while len(block_pool) < total_blocks:
#         block_pool.append(None)

#     random.shuffle(block_pool)  # Trộn ngẫu nhiên

#     # Tạo grid (pattern) từ block_pool
#     layer_1 = [[block_pool.pop() for _ in range(cols)] for _ in range(rows)]
#     layer_2 = [[block_pool.pop() for _ in range(cols)] for _ in range(rows)]

#     return [layer_1, layer_2]

# # Cấu hình game cho từng mức độ khó
# easy_game_config = {
#     "level": 1,
#     "grid_size": (3, 3),
#     "pattern": generate_fixed_pattern(1),  # Gọi hàm tạo pattern cho level 1
#     "time_limit": 60,  # Giới hạn thời gian (giây)
# }

# middle_game_config = {
#     "level": 2,
#     "grid_size": (3, 6),
#     "pattern": generate_fixed_pattern(2),  # Gọi hàm tạo pattern cho level 2
#     "time_limit": 90,  # Giới hạn thời gian (giây)
# }

# hard_game_config = {
#     "level": 3,
#     "grid_size": (6, 6),
#     "pattern": generate_fixed_pattern(3),  # Gọi hàm tạo pattern cho level 3
#     "time_limit": 120,  # Giới hạn thời gian (giây)
# }

import random

# Danh sách động vật
animals = ["Resources/block_icon/alien.jpg", "Resources/block_icon/cheese.png", 
           "Resources/block_icon/coffee.png", "Resources/block_icon/cream.png"]

# Cấu hình Shape và lớp cho từng màn chơi
level_config = {
    1: {
        "shapes": [
            [[1, 1, 1],  # Layer 1
             [1, 1, 1],
             [1, 1, 1]],
            [[1, 1, 1],  # Layer 2
             [1, 1, 1],
             [1, 1, 1]]
        ],
        "time_limit": 60,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0},
            {"x_offset": 10, "y_offset": 20}
        ]
    },
    2: {
        "shapes": [
            [[1, 1, 1, 1, 1, 1],  # Layer 1
             [1, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             ],

            [[1, 1, 0, 0, 1, 1],  # Layer 2
             [1, 1, 0, 0, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             ],

            [[1, 1, 0, 0, 1, 1],  # Layer 3
             [1, 1, 0, 0, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             ],
        ],
        "time_limit": 90,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0},
            {"x_offset": 10, "y_offset": 20},
            
        ]
    },
    3: {
        "shapes": [
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
            {"x_offset": 0, "y_offset": 0},
            {"x_offset": 10, "y_offset": 20},
            {"x_offset": 10, "y_offset": 20},
        ]
    }
}

# Hàm tạo block pool dựa trên tổng số block cần thiết
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

    shapes = config["shapes"]
    total_blocks = sum(sum(row.count(1) for row in shape) for shape in shapes)
    while total_blocks % 3 != 0:  # Đảm bảo bội số của 3
        total_blocks += 1

    block_pool = create_block_pool(total_blocks)

    layers = [fill_layer(shape, block_pool) for shape in shapes]
    return layers

# Tạo config game
def create_game_config(level):
    return {
        "level": level,
        "grid_size": (len(level_config[level]["shapes"][0]), len(level_config[level]["shapes"][0][0])),
        "pattern": generate_pattern(level),
        "time_limit": level_config[level]["time_limit"]
    }

# Ví dụ tạo config cho các màn chơi
easy_game_config = create_game_config(1)
middle_game_config = create_game_config(2)
hard_game_config = create_game_config(3)

# In kết quả
for idx, config in enumerate([easy_game_config, middle_game_config, hard_game_config], start=1):
    print(f"Level {idx} - Time limit: {config['time_limit']}s")
    for i, layer in enumerate(config["pattern"]):
        print(f"Layer {i+1}:")
        for row in layer:
            print(row)
        print()
