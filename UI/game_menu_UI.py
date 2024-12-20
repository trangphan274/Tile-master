import pygame
from Resources.assets import GAME_MENU_PIC_LOADED

def draw_game_menu_ui(screen):
    
    options = ["resume", "replay", "back_home", "quit"]
    
    menu_image = GAME_MENU_PIC_LOADED["menu_board"]
    scale_menu= pygame.transform.scale(menu_image,(600,450))
    screen.blit(scale_menu, (0, 250))  

    font = pygame.font.Font("Resources/font/LuckiestGuy-Regular.ttf", 60)
    text = font.render("Menu", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width()//2, 400)
    screen.blit(text, text_rect)



    button_images = {
        "resume": GAME_MENU_PIC_LOADED["resume"],
        "replay": GAME_MENU_PIC_LOADED["replay"],
        "back_home": GAME_MENU_PIC_LOADED["back_home"],
        "quit": GAME_MENU_PIC_LOADED["quit"]
    }
    button_specs = {
        "resume":    {"x": 170, "y": 450, "w": 80, "h": 80},
        "replay":    {"x": 270, "y": 450, "w": 80, "h": 80},
        "back_home": {"x": 370, "y": 450, "w": 80, "h": 80},
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
                if option == "resume":
                    return "resume"
                elif option == "replay":
                    return "replay"
                elif option == "back_home":
                    return "back_home"
                elif option == "quit":
                    return "quit"


