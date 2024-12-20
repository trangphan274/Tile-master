import pygame
from Resources.assets import BLOCKS_PIC_LOADED,HELPER_PIC_LOADED
from logic.helpersGame import shuffle_blocks,triple_break
from UI.game_menu_UI import draw_game_menu_ui

# Configuration parameters
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (245, 220, 185) # màu nền
GRAY = (50, 50, 50)
BLOCK_SIZE = 50
font = pygame.font.SysFont(None, 36)

animal_images = {name: pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE)) for name, image in BLOCKS_PIC_LOADED.items()}

# contain visibility effects
def draw_blocks_with_images(screen,game, grid_offset):
    
    for block in sorted(game.blocks, key=lambda b: (b.level, b.y, b.x)):
        if block.is_removed or block.status ==0:
            continue

        # Cập nhật vị trí block theo grid_offset
        rect = pygame.Rect(
            block.x + grid_offset[0],  
            block.y + grid_offset[1],  
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
        shadow_color = (100, 100, 100, 100)  
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


def draw_bottom_bar(screen,game):
    
    bottom_bar_image = pygame.image.load('Resources/bar/bottom_bar.png').convert_alpha()

    slot_width = 50 
    slot_spacing = 5
    total_width = 7 * slot_width + 6 * slot_spacing  # Tổng chiều rộng của thanh ngang
    start_x = (SCREEN_WIDTH - total_width) // 2  # Căn giữa theo chiều ngang
    y = SCREEN_HEIGHT - 130  # Vị trí theo chiều dọc (giữ nguyên)

    # Thêm con mèo
    icon_image = pygame.image.load('Resources/bar/cat_on_bar.png').convert_alpha()  # Tải icon với nền trong suốt
    resized_icon = pygame.transform.scale(icon_image, (70, 70))

    icon_x = start_x -12
    icon_y = y -65    
    screen.blit(resized_icon, (icon_x, icon_y))
     
    bottom_bar_image = pygame.transform.scale(bottom_bar_image, (total_width +10, 65))# ép hình

    screen.blit(bottom_bar_image, (start_x-5, y-10)) # nhích hình 
    block_color = (210, 180, 140)

    for i in range(7):
        x = start_x + i * (slot_width + slot_spacing)
        pygame.draw.rect(screen, block_color, (x, y, slot_width, slot_width))
        if i < len(game.selected_blocks):
            block = game.selected_blocks[i]
            animal_image = animal_images.get(block.type_)
            if animal_image:
                screen.blit(animal_image, (x, y))
 


def center_grid(game):
    
    # Tính kích thước grid
    grid_width = max(block.x for block in game.blocks) + BLOCK_SIZE
    grid_height = max(block.y for block in game.blocks) + BLOCK_SIZE
    min_x = min(block.x for block in game.blocks)
    min_y = min(block.y for block in game.blocks)

    # Tính offset để căn giữa
    grid_offset = [
        (SCREEN_WIDTH - grid_width) // 2 - min_x,  # Đảm bảo grid căn giữa đúng
        (SCREEN_HEIGHT - grid_height) // 2 - min_y
    ]
    return grid_offset
#?////////////////////////////////////////////////////////////
# 
#    
def draw_help_buttons(screen, game):
    button_keys=['shuffle','triple']
    button_width = 80
    button_height = 40
    
    
    
    start_x = (SCREEN_WIDTH - 2 * button_width - 2 * 5) // 2 
    y = SCREEN_HEIGHT - 60  

    button_positions = [(start_x + i* (button_width + 5), y) for i in range(2)]
    
    for i, (x, y) in enumerate(button_positions):
            if button_keys[i] in HELPER_PIC_LOADED:  # Đảm bảo helper button tồn tại
                button_image = pygame.transform.scale(
                    HELPER_PIC_LOADED[button_keys[i]], (button_width, button_height)
                )
                screen.blit(button_image, (x, y))
                
            else:
                print(f"Image for button '{button_keys[i]}' not found.")
    
   


    # Kiểm tra sự kiện click
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, (x, y) in enumerate(button_positions):
            
            if x <= mouse_x <= x + button_width and y <= mouse_y <= y + button_height:
                if button_keys[i] == 'shuffle':
                    shuffle_blocks(game,screen)  
                elif button_keys[i] == 'triple':
                    triple_break(game,screen)
                
def draw_game_menu_button(screen,game):

    
    
    button_image = pygame.image.load('Resources/game board/game_menu.png').convert_alpha()
    button_image = pygame.transform.scale(button_image, (60, 60))  # Tùy chỉnh kích thước
    

    # Vị trí nút (góc trên bên trái)
    button_position = (10, 10)
    x, y = button_position
    button_width, button_height = button_image.get_size()

    # Vẽ nút
    screen.blit(button_image, button_position)
    if pygame.mouse.get_pressed()[0]:
        mouse_x,mouse_y = pygame.mouse.get_pos()
        if x<= mouse_x <= x+button_width and y<mouse_y<=y+button_height:
            draw_game_menu_ui(screen)
            return "menu_pressed"


def handle_block_click(screen,pos,game,grid_offset):
    for block in reversed(game.blocks):  # Kiểm tra các block từ trên xuống dưới
        if block.is_removed or not game.is_block_interactable(block):  # Gọi phương thức từ đối tượng game
            continue  # Bỏ qua nếu block bị xóa hoặc không thể tương tác

        rect = pygame.Rect(block.x + grid_offset[0], block.y + grid_offset[1], BLOCK_SIZE, BLOCK_SIZE)

        if rect.collidepoint(pos):  # Nếu người chơi click vào block này
            game.select_block(block,screen)
            block.is_removed = True
            break
    

