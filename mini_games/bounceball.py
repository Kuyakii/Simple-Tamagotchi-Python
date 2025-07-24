import pygame
import random
import time
from constants import *

class BounceBall():
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.title = "Balle rebondissante !"
        self.gain = 0

        self.balls = BB_NB_BALLS
        self.ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.ball_speed_x = self.ball_speed_y = 0
        self.ball_wait = BB_BALL_WAIT
        self.ball_wait_time = 0
        self.ball_waiting = True

        self.bricks = self.load_bricks()

        self.paddle = pygame.Rect(WIDTH // 2, BB_PADDLE_Y, BB_PADDLE_WIDTH, BB_PADDLE_HEIGHT)

    def load_bricks(self):
        bricks = []
        for i in range(BB_NB_BRICK_Y):
            for j in range(BB_NB_BRICK_X):
                brick = pygame.Rect(50 + j * BB_BRICK_MARGIN, BB_BRICK_MARGIN + i * 30, BB_BRICK_WIDTH, BB_BRICK_HEIGHT)
                bricks.append(brick)
        return bricks
    
    def run(self, game, tamagotchi):
        self.game = game
        self.player = tamagotchi
        self.gain = 0
        self.ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.ball_speed_x = self.ball_speed_y = 0
        while self.running:
            self.handle_events()
            self.update()
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

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.paddle.x = mouse_x - self.paddle.width // 2

    def quit(self):
        self.game.paused = False
        self.game.minigaming = False
        self.player.status["playing"] = False
        self.game.money += self.gain
        self.running = False
        self.player.play(self.game.canape)


    def update(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.x < 0 or self.ball.x > WIDTH:
            self.ball_speed_x = -self.ball_speed_x
        if self.ball.y < 0:
            self.ball_speed_y = -self.ball_speed_y

        if self.ball.y > HEIGHT:
            self.balls -= 1
            self.ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
            self.ball_speed_x = 0
            self.ball_speed_y = 0
            pygame.draw.rect(self.screen, RED, self.ball)
            self.ball_waiting = True
        
        if self.ball_waiting:
            self.ball_wait_time += 1
            if self.ball_wait_time >= self.ball_wait:
                self.ball_waiting = False
                self.ball_speed_x = random.choice([-BB_BALL_SPEED, BB_BALL_SPEED])
                self.ball_speed_y = random.choice([-BB_BALL_SPEED, BB_BALL_SPEED])
                self.ball_wait_time = 0
            
        if self.ball.colliderect(self.paddle):
            self.ball_speed_y = -self.ball_speed_y

        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.gain += 1
                self.ball_speed_y = -self.ball_speed_y

        if self.balls <= 0: 
            self.show_message(f"Fin du jeu ! (+{self.gain} coins)")
            time.sleep(2)
            self.quit()

    def draw(self):
        self.screen.fill(SKY_BLUE)
        text = pygame.font.SysFont("Arial", FONT_BIG).render(self.title, True, BLACK)
        self.screen.blit(text, (MINIGAME_BUTTON_X - 10, 10))

        pygame.draw.rect(self.screen, RED, self.ball)
        pygame.draw.rect(self.screen, DARK_BLUE, self.paddle)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BLUE, brick)

        self.draw_score()

    def draw_score(self):
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render(f"Score: {self.gain}", True, BLACK)
        self.screen.blit(text, (10, 10))

        text = pygame.font.SysFont("Arial", FONT_SMALL).render(f"Balles restantes : {self.balls}", True, BLACK)
        self.screen.blit(text, (10, 30))

    def show_message(self, message):
        font = pygame.font.SysFont("Arial", FONT_SMALL)
        text = font.render(message, True, BLACK)
        self.screen.blit(text, (WIDTH // 2 - MINIGAME_WIDTH // 2 + 100, HEIGHT // 2 - MINIGAME_HEIGHT // 2 + 140))
        pygame.display.flip()