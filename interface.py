import pygame
from constants import *

class UIManager:
    def __init__(self, game):
        self.game = game
        self.labels = self.load_labels()
        self.menu_buttons = self.load_menu_buttons()
        self.resume_button = self.load_resume_button()
        self.buttons_environment = self.load_environment_buttons()

    def load_resume_button(self):
        resume_button = pygame.image.load("images/resume_button.png")
        return pygame.transform.scale(resume_button, (IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT))

    def load_menu_buttons(self):
        buttons = [(pygame.image.load("images/pause_button.png"), (IMAGE_SMALL_WIDTH, IMAGE_SMALL_HEIGHT), (WIDTH - MENU_WIDTH // 4, ENVIRONMENT_BUTTON_Y)),
            (pygame.image.load("images/icon_shop.png"), (IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT), (WIDTH - MENU_WIDTH + MENU_BUTTON_MARGIN_LEFT, MENU_BUTTON_MARGIN_TOP))]
        return [(pygame.transform.scale(i[0], i[1]), i[2]) for i in buttons]

    def load_environment_buttons(self):
        return [(pygame.Rect(ENVIRONMENT_BUTTON_MARGIN_LEFT + i * ENVIRONMENT_BUTTON_X,ENVIRONMENT_BUTTON_Y,ENVIRONMENT_BUTTON_WIDTH,ENVIRONMENT_BUTTON_HEIGHT),
                    pygame.font.Font(None, FONT_SMALL).render(ENVIRONMENT_TEXT[i], True, BLACK)) for i in range (NB_ENVIRONNEMENT)]

    def load_labels(self):
        labels = {
            "coins": {"text": lambda: pygame.font.Font(None, FONT_MEDIUM).render(f"Coins : {self.game.money}", True, BLACK),
                    "pos": (COIN_LABEL_X, COIN_LABEL_Y)},
            "croquettes": {"text": lambda:  pygame.font.Font(None, FONT_BIG).render(f"{self.game.croquettes}", True, BLACK),
                    "pos": (CROQUETTES_LABEL_X, CROQUETTES_LABEL_Y)},
            "quit": {"text": lambda: pygame.font.Font(None, FONT_BIG_BIG).render("Quitter", True, BLACK),
                    "pos": (MARGIN_LEFT, ENVIRONMENT_BUTTON_Y // 2)},
            "time": {"text": lambda: pygame.font.Font(None, FONT_BIG).render(f"{self.game.timer // 60}:{self.game.timer % 60}", True, BLACK),
                    "pos": (ENVIRONMENT_BUTTON_MARGIN_LEFT // 2, ENVIRONMENT_BUTTON_Y + IMAGE_MEDIUM_HEIGHT // 3)},
             }
        return labels

    def draw(self, screen):
        self.draw_menu(screen)
        self.draw_labels(screen)
        self.draw_environement_buttons(screen)
        if self.game.paused:
            self.draw_pause(screen)
        if self.game.shop_opened:
            self.draw_shop(screen)

    def draw_menu(self, screen):
        pygame.draw.rect(screen, GREY, (WIDTH - MENU_WIDTH, 0, MENU_WIDTH, HEIGHT))
        self.draw_menu_buttons(screen)

    def draw_labels(self, screen):
        screen.blit(self.labels["coins"]["text"](), self.labels["coins"]["pos"])
        screen.blit(self.labels["croquettes"]["text"](), self.labels["croquettes"]["pos"])
        screen.blit(self.labels["time"]["text"](), self.labels["time"]["pos"])
        
        if self.game.day:
            daynight = pygame.image.load(f"images/icon_day.png")
        else:
            daynight = pygame.image.load(f"images/icon_night.png")
        daynight = pygame.transform.scale(daynight, (IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT))

        croquette = pygame.image.load("images/croquette.png")
        croquette = pygame.transform.scale(croquette, (IMAGE_MEDIUM_WIDTH, IMAGE_MEDIUM_HEIGHT))
        screen.blit(croquette, (MARGIN_LEFT, HEIGHT - croquette.get_height()))
        screen.blit(daynight, (MARGIN_LEFT, ENVIRONMENT_BUTTON_Y))

    def draw_menu_buttons(self, screen):
        for image, pos in self.menu_buttons:
            screen.blit(image, pos)

    def draw_environement_buttons(self, screen): 
        for i, (button_rect, text) in enumerate(self.buttons_environment):
            border_rect = pygame.Rect(button_rect.x + 1, button_rect.y + 1, ENVIRONMENT_BUTTON_WIDTH + 4, ENVIRONMENT_BUTTON_HEIGHT + 4)
            pygame.draw.rect(screen, BLACK, border_rect)
            pygame.draw.rect(screen, LIGHT_RED, button_rect)
            screen.blit(text, (button_rect.x + 10, button_rect.y + 20))
  
    def draw_pause(self, screen):
        gray_surface = pygame.Surface((WIDTH, HEIGHT))
        gray_surface.set_alpha(128)
        gray_surface.fill(GREY)
        screen.blit(gray_surface, BACKGROUND_POS)
        screen.blit(self.resume_button, (WIDTH // 2 - self.resume_button.get_width() // 2, HEIGHT // 2 - self.resume_button.get_height() // 2))

    def draw_shop(self, screen):
        screen.blit(self.game.backgrounds[3], BACKGROUND_POS)
        pygame.draw.rect(screen, RED, (MARGIN_LEFT, ENVIRONMENT_BUTTON_Y - 5, MINIGAME_WIDTH // 2 - 20, MINIGAME_BUTTON_HEIGHT))
        screen.blit(self.labels["quit"]["text"](), self.labels["quit"]["pos"])

        for i,(item, price) in enumerate(self.game.shop_items):
            screen.blit(item, (WIDTH // 4 - 105 + 155 * i, HEIGHT // 2 - 60))
            screen.blit(price, (WIDTH // 4 - 110 + 155 * i, HEIGHT // 2 - 70))

        self.draw_menu(screen)
        screen.blit(self.labels["coins"]["text"](), self.labels["coins"]["pos"])

    