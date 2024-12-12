import random

# Danh sách động vật
animals = ["bird.png", "dog.png", "tree.png", "turtle.png"]

# Hàm tạo pattern cố định cho mỗi màn
def generate_fixed_pattern(level):
    if not animals:  # Kiểm tra xem animals có trống không
        raise ValueError("The animals list is empty!")  # Thông báo lỗi nếu trống

    if level == 1:
        # Pattern hình vuông 3x3, 2 lớp (lớp trên và lớp dưới)
        pattern = [[random.choice(animals) for _ in range(3)] for _ in range(3)]  # lớp trên
        pattern.append([random.choice(animals) for _ in range(9)])  # lớp dưới
    elif level == 2:
        # Pattern random, 3 lớp
        pattern = []
        for _ in range(3):  # 3 lớp
            layer = [random.choice(animals) for _ in range(random.randint(6, 9))]  # random số ô
            pattern.append(layer)
    elif level == 3:
        # Pattern hình tròn, 1 lớp
        pattern = [[random.choice(animals) for _ in range(5)] for _ in range(5)]  # Ví dụ hình tròn
    else:
        # Màn mặc định
        pattern = [[random.choice(animals) for _ in range(7)] for _ in range(7)]  # 1 lớp duy nhất
    
    return pattern


# Hàm hiển thị pattern
def display_pattern(pattern):
    for level in range(len(pattern)):
        print(f"Layer {level + 1}:")
        print(pattern[level])
        print()

# Thử tạo pattern cho màn 1 và màn 2
easy_game_config = {
    "level": 1,
    "pattern": generate_fixed_pattern(1),  # Gọi hàm tạo pattern cho level 1
    "other_config": "value_for_easy_game"  # Các cấu hình khác nếu cần
}

middle_game_config = {
    "level": 2,
    "pattern": generate_fixed_pattern(2),  # Gọi hàm tạo pattern cho level 2
    "other_config": "value_for_middle_game"  # Các cấu hình khác
}

hard_game_config = {
    "level": 3,
    "pattern": generate_fixed_pattern(3),  # Gọi hàm tạo pattern cho level 3
    "other_config": "value_for_hard_game"  # Các cấu hình khác
}

