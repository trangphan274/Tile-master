import pygame
import sys



SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (245, 220, 185) # màu nền
GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER = (100, 149, 237)
FONT_SIZE = 36
BLOCK_SIZE = 50
pygame.init()
font = pygame.font.Font("Resources/font/LuckiestGuy-Regular.ttf", FONT_SIZE)


def menu_UI(screen, on_mode_selected):
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
            draw_button(screen,button["rect"].x, button["rect"].y, button["rect"].width, button["rect"].height, button["text"], is_hovered)

        pygame.display.update()


def draw_button(screen,x, y, w, h, text, is_hovered=False):
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

