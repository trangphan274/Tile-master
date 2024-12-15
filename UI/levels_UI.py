import pygame
from logic.assets import BLOCKS_PIC_LOADED


# Configuration parameters
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
WHITE = (245, 220, 185) # màu nền
GRAY = (50, 50, 50)
BLOCK_SIZE = 50
font = pygame.font.SysFont(None, 36)

animal_images = {name: pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE)) for name, image in BLOCKS_PIC_LOADED.items()}



# Draw blocks with visibility effects
def draw_blocks_with_images(screen,game, grid_offset):
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


def draw_bottom_bar(screen,game):
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
def handle_block_click(pos,game,grid_offset):
    for block in reversed(game.blocks):  # Kiểm tra các block từ trên xuống dưới
        if block.is_removed or not game.is_block_interactable(block):  # Gọi phương thức từ đối tượng game
            continue  # Bỏ qua nếu block bị xóa hoặc không thể tương tác

        rect = pygame.Rect(block.x + grid_offset[0], block.y + grid_offset[1], BLOCK_SIZE, BLOCK_SIZE)

        if rect.collidepoint(pos):  # Nếu người chơi click vào block này
            game.select_block(block)
            block.is_removed = True
            break



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
    

def draw_play_area_border(game):
    if not game.blocks:
        return