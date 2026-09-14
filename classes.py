import pygame
import random as random


#player class
class Player:
    #attributes for player position, rectangle, speed image, and speed
    def __init__(self, x, y, image_stand, image_run_right, image_run_left):
        self.x = x
        self.y = y
        self.image_stand = image_stand
        self.image_run_right = image_run_right
        self.image_run_left = image_run_left
        self.current_image = image_stand
        self.rect = self.current_image.get_rect(midbottom=(self.x, self.y))
        self.speed = 5

    #method to move player WASD
    def move(self, keys, field_rect):
        is_moving = False

        #movement keys, and "animations"
        if keys[pygame.K_d]:
            self.x += self.speed
            self.current_image = self.image_run_right
            is_moving = True
        elif keys[pygame.K_a]:
            self.x -= self.speed
            self.current_image = self.image_run_left
            is_moving = True
            
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.current_image = self.image_run_right
            is_moving = True
        elif keys[pygame.K_s]:
            self.y += self.speed
            self.current_image = self.image_run_left
            is_moving = True
        #stand animation if no movement keys are pressed
        if not is_moving:
            self.current_image = self.image_stand

        # Update rect position based on new X and Y
        self.rect.midbottom = (self.x, self.y)
        
        # Boundary checking against field_rect
        if self.rect.right >= field_rect.right:
            self.rect.right = field_rect.right
            self.x = self.rect.centerx
        if self.rect.left < field_rect.left:
            self.rect.left = field_rect.left
            self.x = self.rect.centerx
        if self.rect.top <= field_rect.top:
            self.rect.top = field_rect.top
            self.y = self.rect.bottom
        if self.rect.bottom >= field_rect.bottom:
            self.rect.bottom = field_rect.bottom
            self.y = self.rect.bottom

    #draw method to blit player image to the screen
    def draw(self, surf):
        surf.blit(self.current_image, self.rect)

class falling_item():
    def __init__(self, x, y, image, speed, item_type):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.item_type = item_type
        # The missing hitbox attribute:
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def update(self):
        self.y += self.speed
        # Update the hitbox position to match the falling image:
        self.rect.midbottom = (self.x, self.y)

    def draw(self, surf):
        surf.blit(self.image, self.rect)

# (Make sure your AttackManager class is pasted right here)

class item_drop_manager():
    def __init__(self, bag_image, health_image):
        self.bag_image = bag_image
        self.health_image = health_image
        self.active_items = []
        self.spawn_item()

    def spawn_item(self):
        """Randomly chooses an item and position, then spawns it."""
        random_x = random.choice([560, 640, 720, 800, 880])
        attack_roll = random.randint(1, 10)
        
        if attack_roll <= 6:
            new_item = falling_item(random_x, 340, self.bag_image, 5, 'bag')
        else:
            new_item = falling_item(random_x, 340, self.health_image, 5, 'heart')
            
        self.active_items.append(new_item)

    def manage_items(self, screen, player):
        damage = 0
        score_diff = 0
        progress_diff = 0
        heal = 0

        for item in self.active_items[:]:
            item.update()
            item.draw(screen)

            # Check collision with the new player object
            if player.rect.colliderect(item.rect):
                if item.item_type == 'bag':
                    score_diff += 500
                    progress_diff += 25
                elif item.item_type == 'heart':
                    heal += 1
                    score_diff += 100
                    
                self.active_items.remove(item)
                self.spawn_item()

            # Check if it hit the floor
            elif item.rect.bottom >= 836:
                if item.item_type == 'bag':
                    damage += 1
                    score_diff -= 100
                    
                self.active_items.remove(item)
                self.spawn_item()

        # Return the math back to the main loop to apply
        return damage, score_diff, progress_diff, heal

#timer class for timed events
class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False

    #activate method to start
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    #deactivate method to stop
    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        """Checks if the timer has finished. Call this in your game loop."""
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()
                return True # Indicates the timer just finished
        return False
    
    def get_time_left(self):
        """Returns the remaining time in seconds."""
        if self.active:
            current_time = pygame.time.get_ticks()
            time_passed = current_time - self.start_time
            time_left = self.duration - time_passed
            
            if time_left < 0:
                time_left = 0
                
            return int(time_left / 1000) # Divide by 1000 for whole seconds
        return 0

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
        pygame.draw.rect(surf, "blue", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surf, "yellow", (self.x, self.y, self.w * ratio, self.h))

class Question:
    def __init__(self, text, options, correct_index):
        self.text = text
        self.options = options
        self.correct_index = correct_index

    def check_answer(self, selected_index):
        """Returns True if the player guessed correctly."""
        return selected_index == self.correct_index

class QuestionManager:
    def __init__(self, font):
        self.font = font
        self.question_pool = [
            Question("What is the truth value of T v F?", ["True", "False", "None", "Both"], 0),
            Question("Which symbol represents a conjunction?", ["v", "^", "~", "->"], 1),
            Question("What is the negation of True?", ["T", "F", "1", "0"], 1)
        ]
        self.option_rects = []
        self.current_question = None

    def get_new_question(self):
        """Picks a random question and removes it from the pool so it won't repeat."""
        if len(self.question_pool) > 0:
            self.current_question = random.choice(self.question_pool)
            self.question_pool.remove(self.current_question)
        else:
            self.current_question = None

    def draw(self, surface):
        """Renders the question and options onto the paper background."""
        if self.current_question:
            self.option_rects.clear()
            # Render the main question text
            q_surf = self.font.render(self.current_question.text, False, 'Black')
            surface.blit(q_surf, (300, 200))

            # Render the 4 options below it
            for i, option in enumerate(self.current_question.options):
                opt_surf = self.font.render(f"{i+1}. {option}", False, 'Blue')
                opt_rect = opt_surf.get_rect(topleft=(350, 300 + i * 60))
                self.option_rects.append((i, opt_rect))
                # Spaces them out vertically by multiplying the index
                surface.blit(opt_surf, opt_rect)
    def click_option(self):
        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0] # Returns 1 if clicking

        for index, rect in self.option_rects:
            # Check for hover AND click
            if rect.collidepoint(mouse) and left_click:
                return index

        return None
        
