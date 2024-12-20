
import pygame
from Resources.assets import RESULT_PIC_LOADED,GAME_MENU_PIC_LOADED


def draw_game_over_screen(screen, is_win):
    result_text ="WIN" if is_win else "LOSE"
    font = pygame.font.Font("Resources/font/LuckiestGuy-Regular.ttf", 60)
    text = font.render(result_text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width()//2, 200)
    screen.blit(text, text_rect)
    
    
    if is_win:
        result_board = RESULT_PIC_LOADED["win_board"]
        result_cat = RESULT_PIC_LOADED["win_cat"]
    else:
        result_board = RESULT_PIC_LOADED["lose_board"]
        result_cat = RESULT_PIC_LOADED["lose_cat"]

    result_board = pygame.transform.scale(result_board, (screen.get_width() // 2, screen.get_height() // 3))
    result_cat = pygame.transform.scale(result_cat, (screen.get_width() // 6, screen.get_height() // 6))

    screen.blit(result_board, (screen.get_width() // 4, screen.get_height() // 6))
    screen.blit(result_cat, (screen.get_width() // 4 + 100, screen.get_height() // 3))  # Điều chỉnh vị trí nếu cần
    
    options = ["replay", "quit"]
    button_images = {
        
        "replay": GAME_MENU_PIC_LOADED["replay"],
        "quit": GAME_MENU_PIC_LOADED["quit"]
    }
    button_specs = {
        "replay":    {"x": 270, "y": 450, "w": 80, "h": 80},        
        "quit":      {"x": 480, "y": 300, "w": 80, "h": 80},
    }
    
    for option in options:
        
        button_spec = button_specs[option]
        x = button_spec["x"]
        y = button_spec["y"]
        w = button_spec["w"]
        h = button_spec["h"]

        button_img = pygame.transform.scale(button_images[option], (w, h))
        screen.blit(button_img, (x, y))
        
    
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_rect = pygame.Rect(x, y, w, h)
            if button_rect.collidepoint(mouse_x, mouse_y):
                if option == "replay":
                    return "replay"
                elif option == "quit":
                    return "quit"