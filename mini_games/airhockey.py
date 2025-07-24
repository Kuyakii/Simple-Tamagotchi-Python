import pygame
import random
import time
from constants import *

class AirHockey:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.title = "AIR HOCKEY !"
        self.gain = 0
        self.puck_x, self.puck_y = WIDTH // 2, HEIGHT // 2
        self.puck_speed_x, self.puck_speed_y = 2.5,2.5
        self.paddle_width, self.paddle_height = 10, 60
        self.paddle_x, self.paddle_y = 50, HEIGHT // 2 - self.paddle_height // 2
        self.paddle_speed = 2.5

    def run(self, game, tamagotchi):
        self.game = game
        self.player = tamagotchi
        self.gain = 0
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                quit_button = pygame.Rect(5, 5, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2)
                if quit_button.collidepoint(mouse_x, mouse_y):
                    self.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.paddle_y -= self.paddle_speed
        if keys[pygame.K_DOWN]:
            self.paddle_y += self.paddle_speed

    def quit(self):
        self.game.paused = False
        self.game.minigaming = False
        self.player.status["playing"] = False
        self.game.money += self.gain
        self.running = False

    def draw(self):
        self.screen.fill(SKY_BLUE)
        text = pygame.font.SysFont("Arial", FONT_BIG).render(self.title, True, BLACK)
        self.screen.blit(text, (MINIGAME_BUTTON_X + 20, 20))

        self.draw_puck()
        self.draw_paddle()
        self.draw_score()
        self.draw_quit_button()

        self.update_puck()

    def draw_puck(self):
        pygame.draw.circle(self.screen, BLACK, (self.puck_x, self.puck_y), 10)

    def draw_paddle(self):
        pygame.draw.rect(self.screen, BLACK, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))

    def draw_score(self):
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render(f"Score: {self.gain}", True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 10, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 10))

    def draw_quit_button(self):
        pygame.draw.rect(self.screen, RED, (5, 5, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2))
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render("Quitter", True, BLACK)
        self.screen.blit(text, (10, 5))

    def update_puck(self):
        self.puck_x += self.puck_speed_x
        self.puck_y += self.puck_speed_y

        if self.puck_x <= 5:
            self.game_over()
        elif self.puck_x > WIDTH:
            self.puck_speed_x = -self.puck_speed_x
        if self.puck_y < 0 or self.puck_y > HEIGHT:
            self.puck_speed_y = -self.puck_speed_y

        if self.puck_x < self.paddle_x + self.paddle_width and self.puck_y > self.paddle_y and self.puck_y < self.paddle_y + self.paddle_height:
            self.puck_speed_x = -self.puck_speed_x
            self.gain += 3

    def game_over(self):
        self.show_message(f"Fin du jeu ! (+{self.gain} coins)")
        self.player.play(self.game.canape)
        time.sleep(2)
        self.quit()

    def show_message(self, message):
        font = pygame.font.SysFont("Arial", FONT_MEDIUM)
        text = font.render(message, True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 100, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 140))
        pygame.display.flip()