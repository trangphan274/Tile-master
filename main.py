import pygame
import sys
from logic.logicGame import Game, dict_to_game_config  # Import Game và hàm chuyển đổi
from logic.levelsGame import default_game_config, easy_game_config, middle_game_config, hard_game_config, lunatic_game_config, sky_game_config, yang_game_config  # Import cấu hình

# Các thông số cấu hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER = (100, 149, 237)
FONT_SIZE = 36
BLOCK_SIZE = 50

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sheep A Sheep")
font = pygame.font.SysFont(None, FONT_SIZE)

# Dữ liệu animals và file ảnh tương ứng
animals = {
    "turtle.png": pygame.image.load("turtle.png"),
    "dog.png": pygame.image.load("dog.png"),
    "tree.png": pygame.image.load("tree.png"),
    "bird.png": pygame.image.load("bird.png")
}
animal_images = {name: pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE)) for name, image in animals.items()}

# Chuyển đổi cấu hình mặc định từ dictionary sang GameConfigType
game = Game(game_config=dict_to_game_config(default_game_config))

# Hàm kiểm tra block bị che khuất (hiệu ứng mờ đen)
def is_block_visible(block, all_blocks):
    for other in all_blocks:
        if other.block_id != block.block_id and other.level > block.level:
            if pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE).colliderect(
                pygame.Rect(other.x, other.y, BLOCK_SIZE, BLOCK_SIZE)
            ):
                return False  # Bị che khuất
    return True

# Hàm vẽ các block với hiệu ứng mờ đen cho các block bị che khuất
def draw_blocks_with_images():
    for block in sorted(game.blocks, key=lambda b: b.level):  # Vẽ theo layer
        if block.is_removed:
            continue

        rect = pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
        animal_image = animal_images[block.type]

        # Kiểm tra nếu block bị che khuất
        if not is_block_visible(block, game.blocks):
            # Vẽ màu đen mờ cho block bị che khuất
            shadow_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 100))  # Màu đen với độ trong suốt
            screen.blit(shadow_surface, rect.topleft)  # Vẽ shadow trước

        screen.blit(animal_image, rect.topleft)  # Vẽ block lên trên shadow

# Hàm vẽ các slot
def draw_slots():
    slot_width = 50
    for i in range(7):
        x = 100 + i * (slot_width + 10)
        y = SCREEN_HEIGHT - 100
        pygame.draw.rect(screen, GRAY, (x, y, slot_width, slot_width))
        if i < len(game.selected_blocks):
            block = game.selected_blocks[i]
            animal_image = animal_images[block.type]
            screen.blit(animal_image, (x, y))

# Hàm xử lý khi click vào block
def handle_block_click(pos):
    for block in reversed(game.blocks):
        if block.is_removed:
            continue

        rect = pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
        if rect.collidepoint(pos):
            game.select_block(block)
            block.is_removed = True  # Đánh dấu block đã được chọn
            break

# Hàm kiểm tra thắng/thua
def check_win_lose():
    if len(game.selected_blocks) > 7:
        print("Game Over: Thanh dưới đầy!")
        pygame.quit()
        sys.exit()

    if game.is_win():
        print("Bạn đã thắng!")
        pygame.quit()
        sys.exit()

# Trang chọn chế độ chơi
def menu_UI(on_mode_selected):
    running = True
    modes = [
        {"name": "简单模式", "key": "easy"},
        {"name": "中等模式", "key": "medium"},
        {"name": "困难模式", "key": "hard"},
        {"name": "地狱模式", "key": "lunatic"},
        {"name": "天狱模式", "key": "sky"},
        {"name": "羊了个羊模式", "key": "yang"}
    ]
    buttons = []
    button_width, button_height = 300, 50
    button_spacing = 20
    start_y = SCREEN_HEIGHT // 4

    for i, mode in enumerate(modes):
        x = (SCREEN_WIDTH - button_width) // 2
        y = start_y + i * (button_height + button_spacing)
        buttons.append({"rect": pygame.Rect(x, y, button_width, button_height), "text": mode["name"], "key": mode["key"]})

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        on_mode_selected(button["key"])
                        return

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            draw_button(button["rect"].x, button["rect"].y, button["rect"].width, button["rect"].height, button["text"], is_hovered)

        pygame.display.update()

# Hàm vẽ nút menu
def draw_button(x, y, w, h, text, is_hovered=False):
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

# Hàm xử lý khi chọn chế độ
def on_mode_selected(mode):
    print(f"Chế độ đã chọn: {mode}")
    # Chuyển đổi cấu hình game tương ứng từ levelsGame.py
    if mode == "easy":
        game_config = easy_game_config
    elif mode == "medium":
        game_config = middle_game_config
    elif mode == "hard":
        game_config = hard_game_config
    elif mode == "lunatic":
        game_config = lunatic_game_config
    elif mode == "sky":
        game_config = sky_game_config
    else:
        game_config = yang_game_config

    # Chuyển đổi cấu hình từ dictionary sang GameConfigType
    global game
    game = Game(game_config=dict_to_game_config(game_config))

# Chạy menu
menu_UI(on_mode_selected)

# Vòng lặp chính
running = True
while running:
    screen.fill(WHITE)

    # Vẽ các block và slots
    draw_blocks_with_images()
    draw_slots()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_block_click(event.pos)

    # Kiểm tra trạng thái game
    check_win_lose()

    pygame.display.update()

pygame.quit()
