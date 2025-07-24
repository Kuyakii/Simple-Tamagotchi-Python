import pygame
from mini_games.rpc import PierreFeuilleCiseaux
from mini_games.airhockey import AirHockey
from mini_games.bounceball import BounceBall
from constants import *

class MiniGame:
    def __init__(self, game):
        self.screen = game.screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.gain = 0
        self.minigames = ["Pierre, Feuille, Ciseaux","Air Hockey","Balle rebondissante"]
        self.game = game
        self.current_game = None

    def run(self, tamagotchi):
        self.tamagotchi = tamagotchi
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
                for i, game in enumerate(self.minigames):
                    button_y =  MINIGAME_BUTTON_Y - i * MINIGAME_BUTTON_Y_SPACE
                    button = pygame.Rect(MINIGAME_BUTTON_X, button_y, MINIGAME_BUTTON_WIDTH, MINIGAME_BUTTON_HEIGHT)
                    if button.collidepoint(mouse_x, mouse_y):
                        if game == "Pierre, Feuille, Ciseaux":
                            self.current_game = PierreFeuilleCiseaux(self.screen)
                        elif game == "Air Hockey":
                            self.current_game = AirHockey(self.screen)
                        elif game == "Balle rebondissante":
                            self.current_game = BounceBall(self.screen)

                        self.current_game.running = True
                        self.running = False
                        self.current_game.run(self.game, self.tamagotchi)

                quit_button = pygame.Rect(WIDTH // 2 - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2)
                if quit_button.collidepoint(mouse_x, mouse_y):
                    self.quit()
                    
    def quit(self):
        self.game.pause = False
        self.game.minigaming = False
        self.tamagotchi.status["playing"] = False
        self.running = False

    def draw(self):
        border_rect = pygame.Rect(WIDTH // 2  - MINIGAME_WIDTH // 2 - 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2 - 2, MINIGAME_WIDTH + 4, MINIGAME_HEIGHT + 4)
        pygame.draw.rect(self.screen, BLACK, border_rect)

        pygame.draw.rect(self.screen, SKY_BLUE, (WIDTH // 2  - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH, MINIGAME_HEIGHT))
        text = pygame.font.SysFont("Arial", FONT_MEDIUM).render("Minigames", True, BLACK)
        self.screen.blit(text, (MINIGAME_BUTTON_X + 80, MINIGAME_LABEL_Y))

        for i, game in enumerate(self.minigames):
            button_y = MINIGAME_BUTTON_Y - i * MINIGAME_BUTTON_Y_SPACE
            border_rect = pygame.Rect(MINIGAME_BUTTON_X - 2, button_y - 2, MINIGAME_BUTTON_WIDTH + 4, MINIGAME_BUTTON_HEIGHT + 4)

            pygame.draw.rect(self.screen, BLACK, border_rect)
            pygame.draw.rect(self.screen, LIGHT_RED, (MINIGAME_BUTTON_X, button_y, MINIGAME_BUTTON_WIDTH, MINIGAME_BUTTON_HEIGHT))
            text = pygame.font.SysFont("Arial", FONT_SMALL).render(game, True, BLACK)
            self.screen.blit(text, (MINIGAME_BUTTON_X + 30, button_y + 10))

        self.draw_quit_button()


    def draw_quit_button(self):
        pygame.draw.rect(self.screen, RED, (WIDTH // 2 - MINIGAME_WIDTH // 2, HEIGHT // 2 - MINIGAME_HEIGHT // 2, MINIGAME_WIDTH // 2 - MINIGAME_BUTTON_WIDTH // 2 + 10, MINIGAME_BUTTON_HEIGHT // 2))
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render("Quitter", True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 5, HEIGHT // 2 - MINIGAME_HEIGHT // 2))
