import pygame
import sys
import random
import math
from button import Button

class Game:
    def __init__(self):
        """
        Initializes the game, screen, assets, and game variables.
        """
        pygame.init()

        # --- Constants ---
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.PLAYER_SPEED = 8
        self.BULLET_SPEED = 10
        self.ENEMY_BASE_SPEED = 5
        self.NUM_ENEMIES = 6

        # --- Screen Setup ---
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Elsu vs Enemy")
        self.clock = pygame.time.Clock()

        # --- Load Assets ---
        self._load_assets()

        # --- Game State Variables ---
        self.top_score = 0
        self.game_state = "main_menu" # Can be 'main_menu', 'playing', 'guidelines'
        self.init_game_variables()

    def _load_assets(self):
        """
        Loads all game assets (images, sounds, fonts).
        """
        # Load Fonts
        self.font_thin = lambda size: pygame.font.Font("assets/fonts/Roboto-Thin.ttf", size)
        self.font_bold = lambda size: pygame.font.Font("assets/fonts/Roboto-Bold.ttf", size)
        
        # Load Sounds
        pygame.mixer.music.load('assets/sounds/background.wav')
        self.bullet_sound = pygame.mixer.Sound('assets/sounds/laser.wav')

        # Load Images
        self.bg_main_menu = pygame.image.load("assets/images/background.png").convert()
        self.bg_gameplay = pygame.image.load("assets/images/background2.png").convert()
        self.bg_guideline = pygame.image.load("assets/images/giao_dien_guide.png").convert()
        self.game_name_img = pygame.image.load("assets/images/game.png").convert_alpha()
        
        self.player_img = pygame.image.load('assets/images/player.png').convert_alpha()
        self.bullet_img = pygame.image.load('assets/images/bullet.png').convert_alpha()
        self.enemy_img = pygame.image.load('assets/images/enemy.png').convert_alpha()

    def init_game_variables(self):
        """
        Resets all variables for a new game session.
        """
        self.player_pos = pygame.Rect(370, 480, self.player_img.get_width(), self.player_img.get_height())
        self.player_x_change = 0

        self.bullet_pos = pygame.Rect(0, 0, self.bullet_img.get_width(), self.bullet_img.get_height())
        self.bullet_state = "rest"  # "rest" or "fire"

        self.score_val = 0

        self.enemies = []
        for _ in range(self.NUM_ENEMIES):
            enemy_rect = pygame.Rect(
                random.randint(0, self.SCREEN_WIDTH - self.enemy_img.get_width()),
                random.randint(50, 150),
                self.enemy_img.get_width(),
                self.enemy_img.get_height()
            )
            self.enemies.append({
                "rect": enemy_rect,
                "x_change": self.ENEMY_BASE_SPEED,
                "y_change": 50
            })
            
    def run(self):
        """
        The main loop that controls the entire application flow.
        """
        pygame.mixer.music.play(-1)
        while True:
            if self.game_state == "main_menu":
                self._main_menu()
            elif self.game_state == "playing":
                self._play_game()
            elif self.game_state == "guidelines":
                self._show_guidelines()

    def _main_menu(self):
        """
        Displays and handles the main menu.
        """
        play_button = Button(image=pygame.image.load("assets/images/playnow.png"), pos=(130, 480),
                             text_input="PLAY NOW", font=self.font_bold(18), base_color=self.WHITE, hovering_color=self.GREEN)
        quit_button = Button(image=pygame.image.load("assets/images/quit.png"), pos=(72, 42),
                             text_input="QUIT", font=self.font_bold(12), base_color="#d7fcd4", hovering_color=self.WHITE)
        how_to_play_button = Button(image=pygame.image.load("assets/images/how_to_play.png"), pos=(95, 420),
                                    text_input="HOW TO PLAY?", font=self.font_bold(12), base_color=self.WHITE, hovering_color=self.GREEN)
        
        while self.game_state == "main_menu":
            self.screen.blit(self.bg_main_menu, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            
            self.screen.blit(self.game_name_img, (40, 128))
            
            top_score_text = self.font_bold(14).render(f"Top Score: {self.top_score}", True, self.WHITE)
            self.screen.blit(top_score_text, (40, 545))

            for button in [play_button, quit_button, how_to_play_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(mouse_pos):
                        self.init_game_variables()
                        self.game_state = "playing"
                    if quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if how_to_play_button.checkForInput(mouse_pos):
                        self.game_state = "guidelines"
            
            pygame.display.update()

    def _play_game(self):
        """
        Handles the main gameplay loop.
        """
        self._handle_events_play()
        self._update_positions()
        self._check_collisions()
        self._draw_elements()
        pygame.display.update()
        self.clock.tick(60) # Limit frame rate

    def _handle_events_play(self):
        """Handles user input during gameplay."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_state = "main_menu"
                if event.key == pygame.K_LEFT:
                    self.player_x_change = -self.PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    self.player_x_change = self.PLAYER_SPEED
                if event.key == pygame.K_SPACE and self.bullet_state == "rest":
                    self.bullet_sound.play()
                    self.bullet_pos.x = self.player_pos.centerx - self.bullet_img.get_width() / 2
                    self.bullet_pos.y = self.player_pos.top
                    self.bullet_state = "fire"
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.player_x_change = 0

    def _update_positions(self):
        """Updates the positions of player, enemies, and bullet."""
        # Update player position
        self.player_pos.x += self.player_x_change
        self.player_pos.x = max(0, min(self.player_pos.x, self.SCREEN_WIDTH - self.player_pos.width))

        # Update bullet position
        if self.bullet_state == "fire":
            self.bullet_pos.y -= self.BULLET_SPEED
            if self.bullet_pos.bottom < 0:
                self.bullet_state = "rest"

        # Update enemy positions
        for enemy in self.enemies:
            enemy["rect"].x += enemy["x_change"]
            if enemy["rect"].left <= 0 or enemy["rect"].right >= self.SCREEN_WIDTH:
                enemy["x_change"] *= -1
                enemy["rect"].y += enemy["y_change"]

    def _check_collisions(self):
        """Checks for collisions between game objects."""
        # Bullet and Enemy collision
        if self.bullet_state == "fire":
            for enemy in self.enemies:
                if self.bullet_pos.colliderect(enemy["rect"]):
                    self.score_val += 1
                    self.bullet_state = "rest"
                    enemy["rect"].x = random.randint(0, self.SCREEN_WIDTH - enemy["rect"].width)
                    enemy["rect"].y = random.randint(30, 200)
                    break
        
        # Player and Enemy collision
        for enemy in self.enemies:
            if enemy["rect"].colliderect(self.player_pos):
                self._game_over()
                return # Exit early to avoid further checks
            if enemy["rect"].bottom >= 450: # Enemy reaches player's horizontal zone
                 if abs(self.player_pos.centerx - enemy["rect"].centerx) < self.player_pos.width / 2:
                     self._game_over()
                     return

    def _draw_elements(self):
        """Draws all game elements to the screen."""
        self.screen.blit(self.bg_gameplay, (0, 0))
        self.screen.blit(self.player_img, self.player_pos)
        
        for enemy in self.enemies:
            self.screen.blit(self.enemy_img, enemy["rect"])
            
        if self.bullet_state == "fire":
            self.screen.blit(self.bullet_img, self.bullet_pos)
            
        score_text = self.font_bold(20).render(f"Points: {self.score_val}", True, self.WHITE)
        self.screen.blit(score_text, (5, 5))

    def _game_over(self):
        """Displays the game over screen and returns to the main menu."""
        if self.score_val > self.top_score:
            self.top_score = self.score_val
            
        game_over_text = self.font_bold(64).render("GAME OVER", True, self.WHITE)
        text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        self.game_state = "main_menu"

    def _show_guidelines(self):
        """Displays the guidelines/how-to-play screen."""
        comeback_button = Button(image=pygame.image.load("assets/images/quit.png"), pos=(72, 42),
                                 text_input="BACK", font=self.font_bold(12), base_color=self.WHITE, hovering_color=self.GREEN)
        
        while self.game_state == "guidelines":
            self.screen.blit(self.bg_guideline, (-1, 0))
            mouse_pos = pygame.mouse.get_pos()
            
            comeback_button.changeColor(mouse_pos)
            comeback_button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if comeback_button.checkForInput(mouse_pos):
                        self.game_state = "main_menu"
                        return
                        
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()