
import random
from logic.assets import BLOCKS_PIC,BLOCKS_PIC_LOADED


#ảnh
block_pic = list(BLOCKS_PIC.values())

#//////
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
            [[1, 0, 1, 1, 0, 1],  # Layer 1: 20
             [0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 1, 0],
             [1, 1, 0, 0, 1, 1],
             [0, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 1, 1, 0, 0],
             ],
            [[0, 0, 1, 1, 0, 0],  # Layer 2: 22 
             [0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0],
             [1, 1, 0, 0, 1, 1],
             [0, 1, 1, 1, 1, 0],
             [0, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 0, 0],
             ],
            [[1, 1, 1, 1, 1, 1],  # Layer 3
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1],
            ],
            [[0, 0, 0, 0, 0, 1],  # Layer 4
             [1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0],
            ]
             
        ],
        "time_limit": 90,
        "layer_offsets":[
            {"x_offset": 0, "y_offset": 0,"padding": 0},
            {"x_offset": 0, "y_offset": 0,"padding": 0},
            {"x_offset": 0, "y_offset": 0,"padding": 0},
            {"x_offset": 0, "y_offset": 0,"padding": 0},
           
            
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

#  block pool dựa trên tổng số block cần để full đủ bảng
def create_block_pool(total_blocks, level):
    if not block_pic:
        raise ValueError("The  list is empty!")
    

    if level == 1:
        num_icons = 3
    elif level == 2:
        num_icons = 9
    elif level == 3:
        num_icons = 12
    else:
        num_icons = len(block_pic)

    block_pool = []
    blocks_per_icon = total_blocks // num_icons

    # Phân phối icon vào block pool
    for i in range(num_icons):
        animal = block_pic[i % len(block_pic)]  # Đảm bảo không vượt quá số icon có sẵn
        count = blocks_per_icon
        block_pool.extend([animal] * count)


    # Tính số dư còn thiếu để thành bội của 3
    missing_blocks = total_blocks - len(block_pool)

# Chỉ thêm đúng số dư còn thiếu
    if missing_blocks > 0:
        for _ in range(missing_blocks):
            block_pool.append(random.choice(block_pic))

    # Đảm bảo danh sách đủ tổng số block và shuffle trước khi trả về
    random.shuffle(block_pool)
    return block_pool


# fill grid theo shape
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
    while total_blocks % 3!= 0:  # Đảm bảo bội số của 3
        total_blocks += 1

    block_pool = create_block_pool(total_blocks,level)

    layers = [fill_layer(shape, block_pool) for shape in pattern]
    return layers

# Tạo config game
def create_game_config(level):
    return {
        "level": level,
        "grid_size": (len(level_config[level]["pattern"][0]), len(level_config[level]["pattern"][0][0])),
        "pattern": generate_pattern(level),
        "time_limit": level_config[level]["time_limit"],
        "layer_offsets": level_config[level].get("layer_offsets", [{"x_offset": 0, "y_offset": 0} for _ in range(len(level_config[level]["pattern"]))]),
        "block_pic": list(BLOCKS_PIC_LOADED.values())    
    }

# Ví dụ tạo config cho các màn chơi
easy_game_config = create_game_config(1)
middle_game_config = create_game_config(2)
hard_game_config = create_game_config(3)