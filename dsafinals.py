import pygame as pygm
import sys as sy
import random as rd
from classes import Player, falling_item, Timer, prog_bar, item_drop_manager, QuestionManager, Question
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



#active phase surfs

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

#question phase surfs

question_surface = pygm.image.load(PROJECT_DIR / 'images' / 'paperbackground.png').convert_alpha()

#pause game surfs

pause_overlay = pygm.Surface((1440, 810), pygm.SRCALPHA)
pause_overlay.fill((0, 0, 0, 128))



bully_rectangle = bully_surface.get_rect(midbottom = (720, bully_y_pos))
pause_rectangle = text_surface.get_rect(topleft = (50, 50))

player_rectangle = player_surface.get_rect(midbottom =(player_x_pos,player_y_pos))
field_rectangle = field_surf.get_rect(midbottom = (720, 810))
lives_rectangle1 = health_surface.get_rect(midbottom = (670, 50))
lives_rectangle2 = health_surface.get_rect(midbottom = (720, 50))
lives_rectangle3 = health_surface.get_rect(midbottom = (770, 50))

question_timer = Timer(7000)

player = Player(720, 710, player_surface_stand, player_run_right_surface, player_run_left_surface)
item_drop = item_drop_manager(bag_surface, health_surface)
question_manager = QuestionManager(font)

progress = prog_bar(250, 200, 300, 40, 100)
progress.prog = 0






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
        screen.blit(bully_surface, (bully_rectangle))
        progress.draw(screen)

#key movement and player blitting
        keys = pygm.key.get_pressed()
        player.move(keys, field_rectangle)
        player.draw(screen)

#attack or heart
        #attack or heart (Handled by the ItemDropManager class)
        damage, score_diff, progress_diff, heal = item_drop.manage_items(screen, player)
        
        # Apply the changes to your global variables
        health_value -= damage
        health_value += heal
        if health_value > 3: 
            health_value = 3
            
        score_num += score_diff
        if score_num < 0:
            score_num = 0
            
        progress.prog += progress_diff
        if progress.prog >= 100:
            game_active = "question"
            progress.prog = 0
            question_timer.activate()
            question_manager.get_new_question()

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
            progress.prog = 0
            


        
            
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
        timer_finished = question_timer.update()
        
        # 1. Draw the background
        screen.blit(question_surface, (0, 0))

        # 2. Let the class render all the text
        question_manager.draw(screen)

        # 3. Handle the timer
        if timer_finished:
            game_active = "active"
            question_timer.deactivate()
            health_value -= 1
        else:
            # 1. Capture the returned index (0, 1, 2, 3, or None)
            selected_index = question_manager.click_option()
            
            # 2. If an option was actually clicked...
            if selected_index is not None:
                # 3. Check if it matches the correct answer
                is_correct = question_manager.current_question.check_answer(selected_index)
                
                # 4. Apply rewards or penalties
                if is_correct:
                    score_num += 1000
                else:
                    health_value -= 1
                    
                # 5. Send the player back to the dodging phase
                game_active = "active"
                question_timer.deactivate()

            # (Keep your timer drawing logic right below this)
            time_left = question_timer.get_time_left()
            time_left = question_timer.get_time_left()
            timer_surface = font.render(f'Time left: {time_left}', False, 'Red')
            timer_rectangle = timer_surface.get_rect(center = (720, 50))
            screen.blit(timer_surface, (timer_rectangle))


    elif game_active == "game_over":
        screen.fill('Black')
        game_over_surface = font.render('Game Over', False, 'Red')
        game_over_rectangle = game_over_surface.get_rect(center = (720, 405))
        screen.blit(game_over_surface, (game_over_rectangle))
        restart_surface = font.render('Restart?', False, 'Blue')
        restart_rectangle = restart_surface.get_rect(center = (720, 480))
        screen.blit(restart_surface, (restart_rectangle))
        item_drop.active_items.clear()
        item_drop.spawn_item()
        mouse = pygm.mouse.get_pos()
        if restart_rectangle.collidepoint(mouse) and pygm.mouse.get_pressed()[0]:
            game_active = "active"
            health_value = 3
            score_num = 0
            player.x = player_x_pos
            player.y = 710
            player.rect.center = (player.x, player.y)
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
