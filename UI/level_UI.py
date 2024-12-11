# import pygame
# import sys

# # Khởi tạo Pygame
# pygame.init()

# # Màn hình
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Game")

# # Màu sắc
# WHITE = (255, 255, 255)
# GRAY = (169, 169, 169)
# GREEN = (0, 255, 0)

# # Các biến trò chơi
# game_status = 0  # 0: chơi, 3: thắng
# clear_block_num = 0
# total_block_num = 10  # Tổng số khối

# # Tạo font
# font = pygame.font.SysFont(None, 36)

# # Khối và khu vực
# blocks = []
# block_width = 50
# block_height = 50
# block_margin = 10

# # Kỹ năng
# skills = {
#     "撤回": None,
#     "移出": None,
#     "洗牌": None,
#     "破坏": None,
#     "圣光": None,
#     "透视": None
# }

# def draw_block(x, y, text, color):
#     pygame.draw.rect(screen, color, pygame.Rect(x, y, block_width, block_height))
#     label = font.render(text, True, (0, 0, 0))
#     screen.blit(label, (x + block_width / 4, y + block_height / 4))

# def draw_victory_message():
#     victory_text = font.render("恭喜，你赢啦！🎉", True, GREEN)
#     screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 2 - 100))

# def update_block_info():
#     global clear_block_num
#     block_info_text = f"块数：{clear_block_num} / {total_block_num}"
#     return font.render(block_info_text, True, (0, 0, 0))

# def reset_game():
#     global clear_block_num, game_status
#     clear_block_num = 0
#     game_status = 0

# # Vòng lặp chính của game
# def game_loop():
#     global game_status, clear_block_num

#     # Các khu vực trò chơi
#     block_positions = [(100 + (i % 5) * (block_width + block_margin), 100 + (i // 5) * (block_height + block_margin)) for i in range(total_block_num)]

#     running = True
#     while running:
#         screen.fill(WHITE)

#         # Kiểm tra sự kiện
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_x, mouse_y = pygame.mouse.get_pos()
#                 for i, (block_x, block_y) in enumerate(block_positions):
#                     if block_x < mouse_x < block_x + block_width and block_y < mouse_y < block_y + block_height:
#                         # Click vào khối
#                         if game_status == 0:  # Nếu đang chơi
#                             clear_block_num += 1
#                             if clear_block_num == total_block_num:
#                                 game_status = 3  # Trò chơi thắng
#                             print(f"Clicked Block {i + 1}")
        
#         # Vẽ các khối
#         for i, (block_x, block_y) in enumerate(block_positions):
#             color = GREEN if game_status != 3 else GRAY  # Khối xanh khi chơi, xám khi thắng
#             draw_block(block_x, block_y, f"Block {i + 1}", color)

#         # Vẽ thông tin khối
#         block_info = update_block_info()
#         screen.blit(block_info, (10, 10))

#         # Vẽ thông báo chiến thắng
#         if game_status == 3:
#             draw_victory_message()

#         # Vẽ các nút kỹ năng (hiện tại chỉ hiển thị văn bản)
#         skill_y = 450
#         for skill_name, skill_action in skills.items():
#             skill_button = font.render(skill_name, True, (0, 0, 0))
#             screen.blit(skill_button, (10, skill_y))
#             skill_y += 40

#         pygame.display.update()

#     pygame.quit()
#     sys.exit()
# ////////////////////////////////////////////////////



