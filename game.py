import pygame
import time
import random
from constants import *
from tamagotchi import Tamagotchi
from minigames import MiniGame
from interface import UIManager
from event import EventManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.tamagotchis = [Tamagotchi(TAMAGOTCHIS[i]) for i in range(NB_TAMAGOTCHIS)]
        self.croquettes = DAILY_CROQUETTES

        self.timer = 0
        self.day = True

        self.shop_opened = False
        self.shop_items = self.load_shop_items()
        self.money = 0
        self.canape = False

        self.minigame = MiniGame(self)
        self.minigaming = False
        self.player = None

        self.paused = False
        self.running = True
        self.temps_ecoule = 0
        self.update_interval = 1000

        self.backgrounds = self.load_backgrounds()
        self.current_background = 0

        self.ui_manager = UIManager(self)
        self.event_manager = EventManager(self)

    def load_backgrounds(self):
        backgrounds = [pygame.image.load("images/salon.jpg"),
                       pygame.image.load("images/salle_a_manger.jpg"),
                        pygame.image.load("images/salle_de_jeux.jpg"),
                        pygame.image.load("images/shop_background.jpg"),]
        return [pygame.transform.scale(image, (WIDTH - MENU_WIDTH, HEIGHT)) for image in backgrounds]

    
    def load_shop_items(self):
        items = [pygame.image.load("images/shop/croquette.png"), pygame.image.load("images/shop/canape.png")]
        return [(pygame.transform.scale(image, (IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT)), pygame.font.Font(None, FONT_MEDIUM).render(f"{SHOP_ITEM_PRICE[i]}", True, BLACK)) for i,image in enumerate(items)]
    
    def run(self):
        while self.running:
            if self.minigaming:
                self.run_minigame()
            self.event_manager.handle_events()
            if not self.paused:
                self.temps_ecoule += 70
                if self.temps_ecoule >= self.update_interval:
                    self.update()
                    self.temps_ecoule -= self.update_interval
            self.draw()

    def run_minigame(self):
        if self.minigaming:
            self.minigame.running = True
            self.minigame.run(self.player)

    def update(self):
        for tamagotchi in self.tamagotchis:
            tamagotchi.update(self.canape)

            if tamagotchi.stats["food"] <= 0 or tamagotchi.stats["health"] <= 0 or tamagotchi.stats["energy"] <= 0:
                self.loose()

            if tamagotchi.status["fight"]:
                for other in self.tamagotchis:
                    other.stats["health"] -= REDUCE_HEALTH_FIGHT

            if tamagotchi.status["playing"]:
                self.paused = True
                self.minigaming = True
                self.player = tamagotchi

        self.timer += 1
        if self.day:
            if self.timer >= DAY_DURATION:
                self.night()
        else:
            if self.timer >= MIN_SLEEP_DURATION:
                self.day = True
                self.timer = 0
       
    def night(self):
        for tamagotchi in self.tamagotchis:
            self.day = False
            self.timer = 0
            tamagotchi.status["awake"] = False
            tamagotchi.stats["sleep_duration"] = random.randint(MIN_SLEEP_DURATION, MAX_SLEEP_DURATION)

    def loose(self):
        self.screen.fill((255, 0, 0))
        font = pygame.font.Font(None, FONT_MEDIUM)
        text = font.render("Vous avez perdu !", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        time.sleep(1)
        self.running = False

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.backgrounds[self.current_background], (0, 0))

        for i, tamagotchi in enumerate(self.tamagotchis):
            x = TAMAGOTCHI_MARGIN_LEFT + i % 3 * TAMAGOTCHI_WIDTH + TAMAGOTCHI_SPACE * i
            y = TAMAGOTCHI_MARGIN_TOP + i // 3 * TAMAGOTCHI_HEIGHT
            tamagotchi.draw(self.screen, x, y)

        self.ui_manager.draw(self.screen)

        pygame.display.flip()

    def open_shop(self):
        self.shop_opened = True
