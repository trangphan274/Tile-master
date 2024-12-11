import pygame
import sys

# Các thông số cấu hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER = (100, 149, 237)
FONT_SIZE = 36

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chọn Chế Độ Chơi")
font = pygame.font.SysFont(None, FONT_SIZE)

# Hàm vẽ nút
def draw_button(x, y, w, h, text, is_hovered=False):
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

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

    # Tạo danh sách các nút
    for i, mode in enumerate(modes):
        x = (SCREEN_WIDTH - button_width) // 2
        y = start_y + i * (button_height + button_spacing)
        buttons.append({"rect": pygame.Rect(x, y, button_width, button_height), "text": mode["name"], "key": mode["key"]})

    while running:
        screen.fill(WHITE)

        # Xử lý sự kiện
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

        # Vẽ các nút
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            draw_button(button["rect"].x, button["rect"].y, button["rect"].width, button["rect"].height, button["text"], is_hovered)

        pygame.display.update()