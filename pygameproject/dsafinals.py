import pygame as pygm
import sys as sy
import random as rd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

pygm.init()
screen = pygm.display.set_mode((1440, 810))
pygm.display.set_caption('Undertale Copy')
clock = pygm.time.Clock()
font = pygm.font.Font(PROJECT_DIR / 'font' / 'BigBadBold BB W00 Regular.ttf', 50)

game_active = "menu"
bag_y_pos = 350
player_x_pos = 720
player_y_pos = 710

bully_y_pos = 340
score_num = 0
attack = 1
health_value = 3

player_surface = pygm.image.load(PROJECT_DIR / 'images' / 'pixel-boy.png').convert_alpha()
player_surface_stand = pygm.image.load(PROJECT_DIR / 'images' / 'pixel-boy.png').convert_alpha()
player_run_right_surface = pygm.image.load(PROJECT_DIR / 'images' / 'boy_run.png').convert_alpha()
player_run_left_surface = pygm.image.load(PROJECT_DIR / 'images' / 'boy_run_left.png').convert_alpha()
background_surface = pygm.image.load(PROJECT_DIR / 'images' / 'background.png').convert()
text_surface = font.render('pause', False, 'Blue')
bully_surface = pygm.image.load(PROJECT_DIR / 'images' / 'professor.png').convert_alpha()
bag_surface = pygm.image.load(PROJECT_DIR / 'images' / 'papernew.png').convert_alpha()
health_surface = pygm.image.load(PROJECT_DIR / 'images' / 'heart.png').convert_alpha()
field_surf = pygm.image.load(PROJECT_DIR / 'images' / 'field_img.png').convert_alpha()

pause_overlay = pygm.Surface((1440, 810), pygm.SRCALPHA)
pause_overlay.fill((0, 0, 0, 128))



bully_rectangle = bully_surface.get_rect(midbottom = (720, bully_y_pos))
pause_rectangle = text_surface.get_rect(topleft = (50, 50))
bag_rectangle = bag_surface.get_rect(midbottom = (720, bag_y_pos))
player_rectangle = player_surface.get_rect(midbottom =(player_x_pos,player_y_pos))
health_rectangle = health_surface.get_rect(midbottom = (720, bag_y_pos))
field_rectangle = field_surf.get_rect(midbottom = (720, 810))
lives_rectangle1 = health_surface.get_rect(midbottom = (670, 50))
lives_rectangle2 = health_surface.get_rect(midbottom = (720, 50))
lives_rectangle3 = health_surface.get_rect(midbottom = (770, 50))


class prog_bar():
    def __init__(self, x, y, w, h, max_prog):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.prog = max_prog
        self.max_prog = max_prog
    def draw (self, surf):
        ratio = self.prog / self.max_prog
        pygm.draw.rect(surf, "blue", (self.x, self.y, self.w, self.h))
        pygm.draw.rect(surf, "yellow", (self.x, self.y, self.w * ratio, self.h))


progress = prog_bar(250, 200, 300, 40, 100)
progress.prog = 0

def random_attack():
    random_attack = rd.randint(1, 10)
    if random_attack <= 9:
        return 1
    elif random_attack ==10:
        return 2
def random_bag():
    random_bagpos = rd.randint(1, 5)
    if random_bagpos == 1:
        bag_rectangle.centerx = 560
    elif random_bagpos == 2:
        bag_rectangle.centerx = 640
    elif random_bagpos == 3:
        bag_rectangle.centerx = 720
    elif random_bagpos == 4:
        bag_rectangle.centerx = 800
    elif random_bagpos == 5:
        bag_rectangle.centerx = 880
def random_health():
    random_healthpos = rd.randint(1, 3)
    if random_healthpos == 1:
            bag_rectangle.centerx = 560
    elif random_healthpos == 2:
            bag_rectangle.centerx = 640
    elif random_healthpos == 3:
            bag_rectangle.centerx = 720
    elif random_healthpos == 4:
            bag_rectangle.centerx = 800
    elif random_healthpos == 5:
            bag_rectangle.centerx = 880
#def hit_warning():



while True:
    for event in pygm.event.get():
        if event.type == pygm.QUIT:
            pygm.quit()
            sy.exit()
    if game_active == "menu":
        screen.fill('Black')
        menu_surface = font.render('Start Game', False, 'Red')
        menu_rectangle = menu_surface.get_rect(center = (720, 405))
        screen.blit(menu_surface, (menu_rectangle))
        mouse = pygm.mouse.get_pos()
        if menu_rectangle.collidepoint(mouse) and pygm.mouse.get_pressed()[0]:
            game_active = "active"

        

    if game_active == "active":    
#background blitting
        screen.blit(background_surface,(0, 0))

#movement keys, player and bully surface blitting
        screen.blit(field_surf, field_rectangle)
        screen.blit(player_surface, player_rectangle)
        screen.blit(bully_surface, (bully_rectangle))
        progress.draw(screen)
        

        left_key = pygm.key.get_pressed()
        if left_key[pygm.K_d]:
            player_rectangle.centerx += 5
            player_surface = player_run_right_surface
            if player_rectangle.right >= field_rectangle.right:
                player_rectangle.right = field_rectangle.right
        if left_key[pygm.K_a]:
            player_rectangle.centerx -= 5
            player_surface = player_run_left_surface
        if player_rectangle.left < field_rectangle.left:
                player_rectangle.left = field_rectangle.left
        left_key = pygm.key.get_pressed()
        if left_key[pygm.K_w]:
            player_rectangle.centery -= 5
            player_surface = player_run_right_surface
            if player_rectangle.top <= field_rectangle.top:
                player_rectangle.top = field_rectangle.top
        if left_key[pygm.K_s]:
            player_rectangle.centery += 5
            player_surface = player_run_left_surface
            if player_rectangle.bottom >= field_rectangle.bottom:
                player_rectangle.bottom = field_rectangle.bottom
        elif left_key[pygm.K_w] == 0 and left_key[pygm.K_s] == 0 and left_key[pygm.K_d] == 0 and left_key[pygm.K_a] == 0:
            player_surface = player_surface_stand

#attack or heart
        if attack == 1:
            screen.blit(bag_surface, (bag_rectangle))
            bag_rectangle.y += 5
            if bag_rectangle.bottom >= 836:
                
                health_value -= 1
                if score_num == 0:
                    score_num = score_num
                else:
                    score_num -= 100
                attack = random_attack()
                bag_rectangle.bottom = 350
                random_bag()
            elif player_rectangle.colliderect(bag_rectangle) == 1:
                attack = random_attack()
                score_num += 500
                progress.prog += 25 
                bag_rectangle.bottom = 350
                random_bag()
                if progress.prog == 100:
                    game_active = "question"
                    progress.prog = 0                
        elif attack == 2:
            screen.blit(health_surface, (health_rectangle))
            health_rectangle.y += 5
            if player_rectangle.colliderect(health_rectangle) == 1:
                if health_value < 3:
                    health_value += 1
                    score_num += 100
                    attack = random_attack()
                    health_rectangle.bottom = 350
                    random_health()
                elif health_value == 3:
                    score_num += 100
                    attack = random_attack()
                    health_rectangle.bottom = 350
                    random_health()
            elif health_rectangle.bottom >= 836:
                attack = random_attack()
                health_rectangle.bottom = 350
                random_health()

#health blitting and game over condition
        if health_value == 3:
            screen.blit(health_surface, (lives_rectangle1))
            screen.blit(health_surface, (lives_rectangle2))
            screen.blit(health_surface, (lives_rectangle3))
            
        elif health_value == 2:
            screen.blit(health_surface, (lives_rectangle1))
            screen.blit(health_surface, (lives_rectangle2))
            
        elif health_value == 1:
            screen.blit(health_surface, (lives_rectangle1))
            
        elif health_value == 0:
            game_active = "game_over"
            


        
            
        mouse = pygm.mouse.get_pos()

    #score surface to display and update score 
    #pag nasa labas ng while loop para hindi mag update ng score every frame

        score_surface = font.render(f'score: {score_num}', False, 'Blue')
        score_rectangle = score_surface.get_rect(topright = (1390, 50))

    #Pause boarders

        pygm.draw.rect(screen, 'White', pause_rectangle, 0 , 20)
        pygm.draw.rect(screen, 'Brown', pause_rectangle, 6, 20)

    #loob din yung if else ng pause hover para mag change ng color kapag hover

        if pause_rectangle.collidepoint(mouse):
            text_surface = font.render('Pause', False, 'Red')
            if pygm.mouse.get_pressed()[0]:
                frozen_screen = screen.copy()
                game_active = "paused"
        elif pause_rectangle.collidepoint(mouse) == 0:
            text_surface = font.render('Pause', False, 'Blue')

    #Display text and score suface sa rectangle location
        
        screen.blit(text_surface, (pause_rectangle))
        screen.blit(score_surface, (score_rectangle))

    #Game over Condition game active == 0 evaluation
    elif game_active == "question":
        screen.fill('Black')
        game_over_surface = font.render('hello this is question', False, 'Red')
        game_over_rectangle = game_over_surface.get_rect(center = (720, 405))
        screen.blit(game_over_surface, (game_over_rectangle))

    elif game_active == "game_over":
        screen.fill('Black')
        game_over_surface = font.render('Game Over', False, 'Red')
        game_over_rectangle = game_over_surface.get_rect(center = (720, 405))
        screen.blit(game_over_surface, (game_over_rectangle))
        restart_surface = font.render('Restart?', False, 'Blue')
        restart_rectangle = restart_surface.get_rect(center = (720, 480))
        screen.blit(restart_surface, (restart_rectangle))
        mouse = pygm.mouse.get_pos()
        if restart_rectangle.collidepoint(mouse) and pygm.mouse.get_pressed()[0]:
            game_active = "active"
            health_value = 3
            score_num = 0
            player_rectangle.midbottom = (player_x_pos, 810)
            attack = random_attack()
    elif game_active == "paused":
        screen.blit(frozen_screen, (0, 0))
        screen.blit(pause_overlay, (0, 0))

        game_paused_surface = font.render('Game Paused', False, 'Red')
        game_paused_rectangle = game_paused_surface.get_rect(center = (720, 405))
        screen.blit(game_paused_surface, (game_paused_rectangle))
        resume_surface = font.render('Resume?', False, 'Blue')
        resume_rectangle = resume_surface.get_rect(center = (720, 480))
        screen.blit(resume_surface, (resume_rectangle))
        mouse = pygm.mouse.get_pos()
        if resume_rectangle.collidepoint(mouse) and pygm.mouse.get_pressed()[0]:
            game_active = "active"

    pygm.display.update()
    clock.tick(60)
