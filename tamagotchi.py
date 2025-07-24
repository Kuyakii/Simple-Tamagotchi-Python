import random
import pygame
from constants import *

class Tamagotchi:

    def __init__(self, name):
        self.name = name
        image = pygame.image.load(f"images/tamagotchis/{self.name}.png")
        self.image = pygame.transform.scale(image, (IMAGE_TAMAGOTCHI_SIZE, IMAGE_TAMAGOTCHI_SIZE))

        self.stats = {
            "food": INITIAL_FOOD,
            "health": INITIAL_HEALTH,
            "enthusiasm": INITIAL_ENTHUSIASM,
            "energy": INITIAL_ENERGY,
            "sleep_duration": random.randint(MIN_SLEEP_DURATION, MAX_SLEEP_DURATION),
            "sleep_timer": 0,
        }

        self.status = {
            "awake": True,
            "fight": False,
            "playing" : False,
            "eating" : False
        }

    def sleep(self,canape):
        mul = 1
        if canape: mul = 3
        self.stats["health"] += GAIN_HEALTH_SLEEP * mul
        self.stats["enthusiasm"] -= REDUCE_ENTHUSIASM_SLEEP
        self.stats["energy"] += GAIN_ENERGY_SLEEP * mul

    def rest(self):
        self.status["awake"] = False
        self.stats["sleep_duration"] = REST_DURATION

    def eat(self):
        if self.status["awake"]:
            if self.stats["food"] + GAIN_FOOD_CROQUETTE >= INITIAL_FOOD:
                self.stats["food"] = INITIAL_FOOD
            else: self.stats["food"] += GAIN_FOOD_CROQUETTE

    def play(self,canape):
        mul = 1
        if canape: mul = 1.5
        if self.status["awake"]:
            if self.stats["enthusiasm"] + GAIN_ENTHUSIASM_PLAY >= INITIAL_ENERGY:
                self.stats["enthusiasm"] = INITIAL_ENTHUSIASM
            else: self.stats["enthusiasm"] += GAIN_ENTHUSIASM_PLAY *mul
            self.stats["energy"] -= REDUCE_ENERGY_PLAY

    def update(self, canape):
        if self.status["awake"]:
            self.stats["food"] -= REDUCE_FOOD_WAKE 

            if self.stats["enthusiasm"] > 0:
                self.stats["enthusiasm"] -= REDUCE_ENTHUSIASM_WAKE 

            if self.stats["enthusiasm"] <= 0:
                self.status["fight"] = True 
            else:
                self.status["fight"] = False
        else:
            self.stats["sleep_timer"] += 1
            if self.stats["sleep_timer"] >= self.stats["sleep_duration"]:
                self.stats["sleep_timer"] = 0
                self.status["awake"] = True
            
            self.sleep(canape)
        
        self.stats["food"] = min(self.stats["food"], INITIAL_FOOD)
        self.stats["health"] = min(self.stats["health"], INITIAL_HEALTH)
        self.stats["enthusiasm"] = min(self.stats["enthusiasm"], INITIAL_ENTHUSIASM)
        self.stats["energy"] = min(self.stats["energy"], INITIAL_ENERGY)
    
    def draw(self, screen, x, y):
        self.draw_image(screen, x, y)
        self.draw_area(screen, x, y)
        self.draw_stats(screen, x, y)
        self.draw_status(screen, x, y)

        y_offset = 0
        y_offset = self.draw_buttons(screen, x, y, y_offset)
    
    def draw_image(self, screen, x, y):
        screen.blit(self.image, (x+10, y))

    def draw_area(self, screen, x, y):
        rectangle_width = self.image.get_width() 
        rectangle_height = self.image.get_height() 
        pygame.draw.rect(screen, BLACK, (x, y - rectangle_height * .85, rectangle_width * 2, rectangle_height * 1.9), 2)

    def draw_status(self, screen, x, y):
        x+=5
        nb_status = 0
        for key, value in self.status.items():
            if value == True and key != "awake":
                nb_status += 1

        if self.status["awake"]:
            image = pygame.image.load(f"images/icon_day.png")
        else:
            image = pygame.image.load(f"images/icon_night.png")
        image = pygame.transform.scale(image, (STATUS_SIZE, STATUS_SIZE))

        screen.blit(image, (x + STATUS_MARGIN_LEFT - nb_status * STATUT_SPACE, y + STATUS_MARGIN_TOP))

        if self.status["fight"]:
            image = pygame.image.load(f"images/icon_angry.jpg")
            image = pygame.transform.scale(image, (STATUS_SIZE, STATUS_SIZE))
            screen.blit(image, (x + STATUS_MARGIN_LEFT * 3 - nb_status * STATUT_SPACE, y + STATUS_MARGIN_TOP))

    def draw_stats(self, screen, x, y):
        font = pygame.font.Font(None, FONT_MEDIUM)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (x+NAME_MARGIN_LEFT, y+NAME_MARGIN_TOP))

        stats_labels = STATS

        for i, label in enumerate(stats_labels):
            value = self.stats[label.lower()]
            width = int(value / INITIAL_HEALTH * STAT_WIDTH)
            color = BARRE_COLORS[label.lower()]

            border_width = 2
            pygame.draw.rect(screen, BLACK, (x + STAT_OFFSET_X, y + STAT_OFFSET_Y + i * STAT_SPACE, STAT_WIDTH + 2 * border_width, STAT_HEIGHT), border_width)
            pygame.draw.rect(screen, color, (x + STAT_OFFSET_X + border_width, y + STAT_OFFSET_Y + i * STAT_SPACE + border_width, width, STAT_HEIGHT - 2 * border_width))

    def draw_buttons(self, screen, x, y, y_offset):

        button_x = x + BUTTON_MARGIN_LEFT
        button_y = y + y_offset

        if not self.status["awake"]:
            font = pygame.font.Font(None, FONT_SMALL - 3)
            text_surfaces = []
            text_lines = [f"{self.name} est en", "train de dormir !", "Il ne peut pas", "jouer, manger ou", "faire une sieste."]
            for line in text_lines:
                text_surface = font.render(line, True, BLACK)
                text_surfaces.append(text_surface)

            text_rects = []
            current_y = button_y
            for text_surface in text_surfaces:
                text_rect = text_surface.get_rect(center=(button_x+27, current_y+10))
                text_rects.append(text_rect)
                current_y += text_rect.height + 5

            for text_surface, text_rect in zip(text_surfaces, text_rects):
                screen.blit(text_surface, text_rect)

            return y_offset

        for i in range(len(BUTTON_TEXTS)):
            border_rect = pygame.Rect(button_x - 2, button_y - 2, BUTTON_WIDTH + 4, BUTTON_HEIGHT + 4)
            pygame.draw.rect(screen, BLACK, border_rect)
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, BUTTON_COLORS[i], button_rect)
            font = pygame.font.Font(None, FONT_SMALL)
            text = font.render(BUTTON_TEXTS[i], True, BLACK)
            screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
            button_y += BUTTON_HEIGHT + BUTTON_SPACING

        return y_offset + len(BUTTON_TEXTS) * (BUTTON_HEIGHT + BUTTON_SPACING)
