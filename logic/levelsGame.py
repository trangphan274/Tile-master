
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
            [[0, 1, 1, 1, 1, 0],  # head
             [1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 0],
             [0, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 1, 1, 0, 0],
             [0, 0, 1, 1, 0, 0],
            ],
            [[0, 1, 1, 1, 1, 1],  # body 1
             [0, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1],
             [0, 1, 1, 0, 1, 1],
            ],
            [[1, 1, 1, 1, 1, 1, 1, 1],  # body 2
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
            ],
           
            [ #hand
             [0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0],
            ],
            [ #hand
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 1],
            ]
             
             
             
             
        ],
        "time_limit": 90,
        "layer_offsets":[
            {"x_offset": 130, "y_offset": 180,"padding": 0}, 
            {"x_offset": 110, "y_offset": 420,"padding": 0},
            {"x_offset": 85, "y_offset": 350,"padding": 0},  
            
            {"x_offset": 10, "y_offset": 300,"padding": 50},
            {"x_offset": 10, "y_offset": 300,"padding": 50},
           
            
        ]
    },
    3: {
        "pattern": [
            [
             [1, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 0, 1, 1, 1],  # Layer bottom: 48
             [1, 1, 1, 0, 0, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 1, 1, 0, 0],

             ],

            [
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 0, 0, 0, 1, 1],  # Layer 36
             [0, 1, 1, 0, 0, 0, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 1, 1, 0, 0, 0],
             ],
             [
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 0, 0, 1, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 1, 1, 1, 1, 0, 0],
             [0, 0, 0, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             ],
             [
             [0, 0, 0, 0, 0, 0, 0, 0], #12
             [0, 0, 0, 0, 0, 0, 0, 0], # top
             [0, 0, 1, 0, 0, 1, 0, 0],
             [0, 0, 1, 1, 1, 1, 0, 0],
             [0, 0, 1, 1, 1, 1, 0, 0],
             [0, 0, 0, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             ]

        ],
        "time_limit": 300,
        "layer_offsets":[
            {"x_offset": 10, "y_offset": 10,"padding": 10},
            {"x_offset": 30, "y_offset": 50,"padding": 0},
            {"x_offset": 50, "y_offset": 55,"padding": 0},
            {"x_offset": 40, "y_offset": 80,"padding": 3}
        ]
    }
}

#  block pool 
def create_block_pool(total_blocks, level):
    if not block_pic:
        raise ValueError("The block_pic list is empty!")
    
    # Đặt số icon dựa trên level
    if level == 1:
        num_icons = 3
    elif level == 2:
        num_icons = min(11, total_blocks // 3)  # Giới hạn  lai num_icons 
    elif level == 3:
        num_icons = min(15, total_blocks // 3)  
    else:
        num_icons = min(len(block_pic), total_blocks // 3)

    block_pool = []
    blocks_per_icon = (total_blocks // 3) // num_icons * 3  # bội 3

    # Phân phối icon 
    for i in range(num_icons):
        animal = block_pic[i % len(block_pic)]
        block_pool.extend([animal] * blocks_per_icon)

    # Tính số dư còn thiếu
    current_blocks = len(block_pool)
    missing_blocks = total_blocks - current_blocks

    # Bổ sung các block dư theo bội số của 3
    if missing_blocks > 0:
        for i in range(0, missing_blocks, 3):
            animal = block_pic[i % len(block_pic)]
            block_pool.extend([animal] * 3)

    # Đảm bảo tổng là bội của 3
    while len(block_pool) % 3 != 0:
        block_pool.append(random.choice(block_pic))

    # Shuffle trước khi trả về
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
# shuffle khó cho 1 số màn 

def shuffle_difficult(block_pool):
    random.shuffle(block_pool)
    new_pool= []
    pairs =[]
    #gom lại theo cặp 
    while len(block_pool)>=2:
        pair =[block_pool.pop(),block_pool.pop()]
        pairs.append(pair)
    # Rải cặp và block lẻ
    for pair in pairs:
        new_pool.extend(pair)
        if block_pool:
            new_pool.append(block_pool.pop())
    # suffle lại 1 lần nữa
    random.shuffle(new_pool)
    return new_pool

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
    difficult_levels=[3]
    if level in difficult_levels:
        block_pool = shuffle_difficult(block_pool)
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