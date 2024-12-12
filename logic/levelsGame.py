import random

# Danh sách động vật
animals = ["bird.png", "dog.png", "tree.png", "turtle.png"]

# Hàm tạo pattern cố định cho mỗi màn
def generate_fixed_pattern(level):
    if not animals:
        raise ValueError("The animals list is empty!")

    # Xác định kích thước grid theo level
    grid_size = {
        1: (3, 3),  # Level 1: 3x3 grid
        2: (3, 6),  # Level 2: 3x6 grid
        3: (6, 6)   # Level 3: 6x6 grid
    }.get(level, (3, 3))  # Default 3x3 grid nếu level không xác định

    rows, cols = grid_size
    total_blocks = rows * cols
    total_blocks_needed = total_blocks * 2  # Tổng số block cần cho 2 lớp

    # Đảm bảo tổng số block là bội số của 3
    if total_blocks_needed % 3 != 0:
        raise ValueError("The total number of blocks (rows * cols * layers) must be divisible by 3.")

    # Tạo block pool sao cho mỗi loại icon có số lượng chia hết cho 3
    block_pool = []
    blocks_per_icon = total_blocks_needed // len(animals)

    for animal in animals:
        # Đảm bảo số lượng của mỗi icon chia hết cho 3
        count = blocks_per_icon
        if count % 3 != 0:
            count += 3 - (count % 3)
        block_pool.extend([animal] * count)

    # Đảm bảo số block trong pool không vượt quá tổng cần thiết
    block_pool = block_pool[:total_blocks_needed]
    random.shuffle(block_pool)  # Trộn ngẫu nhiên

    # Tạo grid (pattern) từ block_pool
    # Lớp 1
    layer_1 = [[block_pool.pop() for _ in range(cols)] for _ in range(rows)]

    # Lớp 2 (ít block hơn để tạo cảm giác chồng)
    layer_2 = [[block_pool.pop() if random.random() > 0.5 else None for _ in range(cols)] for _ in range(rows)]

    return [layer_1, layer_2]

# Cấu hình game cho từng mức độ khó
easy_game_config = {
    "level": 1,
    "grid_size": (3, 3),
    "pattern": generate_fixed_pattern(1),  # Gọi hàm tạo pattern cho level 1
    "time_limit": 60,  # Giới hạn thời gian (giây)
}

middle_game_config = {
    "level": 2,
    "grid_size": (3, 6),
    "pattern": generate_fixed_pattern(2),  # Gọi hàm tạo pattern cho level 2
    "time_limit": 90,  # Giới hạn thời gian (giây)
}

hard_game_config = {
    "level": 3,
    "grid_size": (6, 6),
    "pattern": generate_fixed_pattern(3),  # Gọi hàm tạo pattern cho level 3
    "time_limit": 120,  # Giới hạn thời gian (giây)
}

# Các config này có thể được import từ file khác để sử dụng
