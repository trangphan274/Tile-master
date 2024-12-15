import pygame
import sys
from logic.logicGame import Game, dict_to_game_config
from logic.levelsGame import easy_game_config, middle_game_config, hard_game_config
from logic.assets import BLOCKS_PIC_LOADED


# Configuration parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (245, 220, 185) # màu nền
GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER = (100, 149, 237)
FONT_SIZE = 36
BLOCK_SIZE = 50


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sheep A Sheep")
font = pygame.font.SysFont(None, FONT_SIZE)



animal_images = {name: pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE)) for name, image in BLOCKS_PIC_LOADED.items()}

# bắt đầu game (default)
game = None

# Draw blocks with visibility effects
def draw_blocks_with_images():
    for block in sorted(game.blocks, key=lambda b: (b.level, b.y, b.x)):
        if block.is_removed:
            continue

        # Cập nhật vị trí block theo grid_offset
        rect = pygame.Rect(
            block.x + grid_offset[0],  # Thêm offset vào tọa độ x
            block.y + grid_offset[1],  # Thêm offset vào tọa độ y
            BLOCK_SIZE,
            BLOCK_SIZE
        )
        block.type_ = block.type_.split('/')[-1].split('.')[0]
        animal_image = animal_images.get(block.type_)
        if not animal_image:
            print(f"Error: No image found for block type {block.type_}")
            continue

        # Đổ bóng
        shadow_offset = 5
        shadow_color = (100, 100, 100, 100)  # Màu xám nhạt với độ trong suốt
        shadow_rect = rect.move(shadow_offset, shadow_offset)
        shadow_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, shadow_color, (0, 0, BLOCK_SIZE, BLOCK_SIZE), border_radius=8)
        screen.blit(shadow_surface, shadow_rect.topleft)

        # Vẽ hình ảnh block
        if animal_image:
            animal_image.set_alpha(100 if not game.is_block_visible(block) else 255)
            animal_image = pygame.transform.smoothscale(animal_image, (BLOCK_SIZE, BLOCK_SIZE))

            # Tạo surface để chứa ảnh đã bo góc
            image_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            image_surface.blit(animal_image, (0, 0))

            # Tạo mask bo góc
            mask = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (0, 0, BLOCK_SIZE, BLOCK_SIZE), border_radius=8)
            image_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Vẽ ảnh
            screen.blit(image_surface, rect.topleft)
            pygame.draw.rect(screen, (0, 0, 0), rect, width=1, border_radius=8)  # Viền và bo góc

        # Vẽ viền đen cho bóng đổ
        pygame.draw.rect(screen, (0, 0, 0), rect, width=1, border_radius=8)

# Vẽ thanh ngang 
def draw_bottom_bar():
    slot_width = 50  # Kích thước của mỗi slot
    slot_spacing = 5  # Khoảng cách giữa các slot
    total_width = 7 * slot_width + 6 * slot_spacing  # Tổng chiều rộng của thanh ngang
    start_x = (SCREEN_WIDTH - total_width) // 2  # Căn giữa theo chiều ngang
    y = SCREEN_HEIGHT - 100  # Vị trí theo chiều dọc (giữ nguyên)

    for i in range(7):
        x = start_x + i * (slot_width + slot_spacing)
        pygame.draw.rect(screen, GRAY, (x, y, slot_width, slot_width))
        if i < len(game.selected_blocks):
            block = game.selected_blocks[i]
            animal_image = animal_images.get(block.type_)
            if animal_image:
                screen.blit(animal_image, (x, y))

# Hàm xử lý click block
def handle_block_click(pos):
    for block in reversed(game.blocks):  # Kiểm tra các block từ trên xuống dưới
        if block.is_removed or not game.is_block_interactable(block):  # Gọi phương thức từ đối tượng game
            continue  # Bỏ qua nếu block bị xóa hoặc không thể tương tác

        rect = pygame.Rect(block.x + grid_offset[0], block.y + grid_offset[1], BLOCK_SIZE, BLOCK_SIZE)

        if rect.collidepoint(pos):  # Nếu người chơi click vào block này
            game.select_block(block)
            block.is_removed = True
            break



def center_grid():
    global grid_offset
    # Tính kích thước grid
    grid_width = max(block.x for block in game.blocks) + BLOCK_SIZE
    grid_height = max(block.y for block in game.blocks) + BLOCK_SIZE
    min_x = min(block.x for block in game.blocks)
    min_y = min(block.y for block in game.blocks)

    # Tính offset để căn giữa
    grid_offset = [
        (SCREEN_WIDTH - (grid_width - min_x)) // 2 - min_x,
        (SCREEN_HEIGHT - (grid_height - min_y)) // 2 - min_y
    ]

# Check win/lose conditions
def check_win_lose():
    if len(game.selected_blocks) == 7:
        print("Game Over: Slots are full!")
        pygame.quit()
        sys.exit()

    if game.is_win():
        print("You Win!")
        pygame.quit()
        sys.exit()

# Game mode selection menu
def menu_UI(on_mode_selected):
    running = True
    modes = [
        {"name": "Easy Mode", "key": "easy"},
        {"name": "Medium Mode", "key": "medium"},
        {"name": "Hard Mode", "key": "hard"}
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

# vẽ nút
def draw_button(x, y, w, h, text, is_hovered=False):
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

# Hchọn màn
def on_mode_selected(mode):
    print(f"Selected mode: {mode}")
    if mode == "easy":
        game_config = easy_game_config
    elif mode == "medium":
        game_config = middle_game_config
    else:
        game_config = hard_game_config

    global game
    game = Game(game_config=dict_to_game_config(game_config))
    print(f"Game initialized with {len(game.blocks)} blocks.")
    center_grid()

def draw_play_area_border():
    # Xác định giới hạn khu vực chơi dựa trên các block
    if not game.blocks:
        return  # Nếu chưa có block, không vẽ

    # Lấy giới hạn x và y từ các block
    min_x = min(block.x for block in game.blocks)
    max_x = max(block.x for block in game.blocks) + BLOCK_SIZE
    min_y = min(block.y for block in game.blocks)
    max_y = max(block.y for block in game.blocks) + BLOCK_SIZE

   
    
# Run the menu
menu_UI(on_mode_selected)

# Ensure game is initialized before entering main loop
if game is None:
    print("Game configuration not loaded correctly.")
    pygame.quit()
    sys.exit()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    draw_play_area_border() 
    draw_blocks_with_images()
    draw_bottom_bar()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_block_click(event.pos)

    # Check game status
    check_win_lose()

    pygame.display.update()

pygame.quit()