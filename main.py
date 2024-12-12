import pygame
import sys
from logic.logicGame import Game, dict_to_game_config
from logic.levelsGame import easy_game_config, middle_game_config, hard_game_config

# Configuration parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_HOVER = (100, 149, 237)
FONT_SIZE = 36
BLOCK_SIZE = 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sheep A Sheep")
font = pygame.font.SysFont(None, FONT_SIZE)

# Load animal images
animals = {
    "turtle.png": pygame.image.load("turtle.png"),
    "dog.png": pygame.image.load("dog.png"),
    "tree.png": pygame.image.load("tree.png"),
    "bird.png": pygame.image.load("bird.png")
}
animal_images = {name: pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE)) for name, image in animals.items()}

# Initialize Game with default config
game = None



# Draw blocks with visibility effects
def draw_blocks_with_images():
    for block in sorted(game.blocks, key=lambda b: (b.level, b.y, b.x)):
        if block.is_removed:
            continue

        rect = pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
        animal_image = animal_images.get(block.type_)

        if animal_image:
            animal_image.set_alpha(100 if not game.is_block_visible(block) else 255)
            screen.blit(animal_image, rect.topleft)

# Draw slots at the bottom of the screen
def draw_slots():
    slot_width = 50
    for i in range(7):
        x = 100 + i * (slot_width + 10)
        y = SCREEN_HEIGHT - 100
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

        rect = pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
        if rect.collidepoint(pos):  # Nếu người chơi click vào block này
            game.select_block(block)
            block.is_removed = True
            break


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

# Draw a button with hover effect
def draw_button(x, y, w, h, text, is_hovered=False):
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

# Handle game mode selection
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

    # Draw blocks and slots
    draw_blocks_with_images()
    draw_slots()

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