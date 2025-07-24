import pygame
from constants import *

class EventManager:
    def __init__(self, game):
        self.game = game
        self.ui_manager = game.ui_manager

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game.paused:
                    self.handle_mouse_click(event.pos)
                else:
                    self.handle_pause_click(event.pos)

                if self.game.shop_opened:
                    self.handle_shop_click(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def handle_pause_click(self, pos):
        resume_rect = pygame.Rect(
            WIDTH // 2 - self.ui_manager.resume_button.get_width() // 2,
            HEIGHT // 2 - self.ui_manager.resume_button.get_height() // 2,
            self.ui_manager.resume_button.get_width(),
            self.ui_manager.resume_button.get_height(),
        )
        if resume_rect.collidepoint(pos):
            self.game.paused = False

    def handle_shop_click(self, pos):
        quit_rect = pygame.Rect(MARGIN_LEFT, ENVIRONMENT_BUTTON_Y - 5, MINIGAME_WIDTH // 2 - 20, MINIGAME_BUTTON_HEIGHT)
        if quit_rect.collidepoint(pos):
            self.game.shop_opened = False
            self.game.paused = False
        
        for i in range (len(self.game.shop_items)):
            rect = pygame.Rect(WIDTH // 4 - 105 + 155 * i, HEIGHT // 2 - 60, IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT)
            if rect.collidepoint(pos):
                if self.game.money - SHOP_ITEM_PRICE[i] >= 0:
                    self.game.money -= SHOP_ITEM_PRICE[i]
                    if i == 0:
                        self.game.croquettes +=1
                    elif i == 1:
                        self.game.canape = True

    def handle_mouse_click(self, pos):
        for i, tamagotchi in enumerate(self.game.tamagotchis):
            x = TAMAGOTCHI_MARGIN_LEFT + i % 3 * TAMAGOTCHI_WIDTH + TAMAGOTCHI_SPACE * i
            button_y = TAMAGOTCHI_MARGIN_TOP + i // 3 * TAMAGOTCHI_HEIGHT
            button_x = x + BUTTON_MARGIN_LEFT

            button_eat = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(self.game.screen, BLACK, button_eat)
            button_y += BUTTON_HEIGHT + BUTTON_SPACING
            button_play = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            button_y += BUTTON_HEIGHT + BUTTON_SPACING
            button_sleep = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

            if button_eat.collidepoint(pos) and tamagotchi.status["awake"]:
                tamagotchi.eat()
                self.game.croquettes -= 1

            elif button_play.collidepoint(pos) and tamagotchi.status["awake"]:
                tamagotchi.status["playing"] = True

            elif button_sleep.collidepoint(pos) and tamagotchi.status["awake"]:
                tamagotchi.rest()

        for i, button in enumerate(self.ui_manager.buttons_environment):
            if button[0].collidepoint(pos):
                self.game.current_background = i

        pause_rect = pygame.Rect(WIDTH - 70, 10, IMAGE_SMALL_WIDTH, IMAGE_SMALL_HEIGHT)
        if pause_rect.collidepoint(pos):
            self.game.paused = True

        shop_rect = pygame.Rect(WIDTH - 270, 120, 100, 100)
        if shop_rect.collidepoint(pos):
            self.game.paused = True
            self.game.open_shop()

