import pygame
import random
import time
from constants import *

class PierreFeuilleCiseaux():
    def __init__(self, screen):
        self.choices = ["pierre", "feuille", "ciseaux"]
        self.player_choice = self.player_image = None
        self.screen = screen
        self.running = True
        self.title = "PIERRE, FEUILLE, CISEAUX !"

        self.gain = 0

        images = [pygame.image.load("images/minigames/pierre.png"), pygame.image.load("images/minigames/feuille.png"), pygame.image.load("images/minigames/ciseaux.png")]
        self.images = [pygame.transform.scale(image, RPC_ICON_SIZE) for image in images]

        self.rects = [pygame.Rect(WIDTH // 2 - MINIGAME_WIDTH // 2 + 100 + i * 110, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 60, 100, 100) for i in range(3)]

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

                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.player_choice = self.choices[i]
                        self.player_image = self.images[i]

                        self.robot_choice = random.choice(self.choices)
                        self.robot_image = pygame.image.load(f"images/minigames/{self.robot_choice}.png")

                quit_button = pygame.Rect(WIDTH // 2 - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2)
                if quit_button.collidepoint(mouse_x, mouse_y):
                    self.quit()

    def draw(self):
        pygame.draw.rect(self.screen, SKY_BLUE, (WIDTH // 2  - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH, MINIGAME_HEIGHT))
        text = pygame.font.SysFont("Arial", FONT_MEDIUM).render(self.title, True, BLACK)
        self.screen.blit(text, (MINIGAME_BUTTON_X + 20, MINIGAME_LABEL_Y))

        for i, image in enumerate(self.images):
            self.screen.blit(image, self.rects[i])

        if self.player_choice is not None:
            pygame.draw.rect(self.screen, LIGHT_RED, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 100, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 200, 100, 100))
            self.player_image = pygame.transform.scale(self.player_image, (100, 100))
            self.screen.blit(self.player_image, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 100, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 200))

            pygame.draw.rect(self.screen, LIGHT_RED, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 300, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 200, 100, 100))
            self.robot_image = pygame.transform.scale(self.robot_image, (100, 100))
            self.screen.blit(self.robot_image, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 300, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 200))
            self.determine_winner()


        self.draw_quit_button()
    
    def quit(self):
        self.game.paused = False
        self.game.minigaming = False
        self.player.status["playing"] = False
        self.game.money += self.gain
        self.running = False

    def draw_quit_button(self):
        pygame.draw.rect(self.screen, RED, (WIDTH // 2 - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2))
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render("Quitter", True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 5, HEIGHT // 2 - MINIGAME_HEIGHT // 2))

    def determine_winner(self):
        if self.player_choice == self.robot_choice:
            self.show_message("Égalité !")
        elif (self.player_choice == "pierre" and self.robot_choice == "ciseaux") or \
             (self.player_choice == "feuille" and self.robot_choice == "pierre") or \
             (self.player_choice == "ciseaux" and self.robot_choice == "feuille"):
            self.gain = 10
            self.show_message(f"{self.player.name} a gagné ! (+10 coins)")
        else:
            self.show_message(f"{self.player.name} a perdu !")

        time.sleep(2)
        self.player.play(self.game.canape)
        self.quit()

    def show_message(self, message):
        font = pygame.font.SysFont("Arial", FONT_MEDIUM)
        text = font.render(message, True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 100, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 140))
        pygame.display.flip()