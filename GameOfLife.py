import pygame
import numpy as np
import pickle

class GameOfLife:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameOfLife, cls).__new__(cls)
        return cls._instance

    def __init__(self, width, height, n_cells_x, n_cells_y):
        if not hasattr(self, 'initialized'):
            self.width, self.height = width, height
            self.screen = pygame.display.set_mode((width, height))
            self.n_cells_x, self.n_cells_y = n_cells_x, n_cells_y
            self.cell_width = width // n_cells_x
            self.cell_height = height // n_cells_y
            self.game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])
            self.running = True
            self.paused = False
            self.tick_interval = 1  
            self.clock = pygame.time.Clock()
            self.initialized = True

    def save_state(self, filename="game_state.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump({
                'game_state': self.game_state,
                'paused': self.paused
            }, f)

    def load_state(self, filename="game_state.pkl"):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.game_state = data['game_state']
            self.paused = data['paused']

    def toggle_pause(self):
        self.paused = not self.paused

    def draw_button(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (self.width - 200, self.height - 60, 200, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Next Generation", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width - 100, self.height - 35))
        self.screen.blit(text, text_rect)

    def draw_grid(self):
        for y in range(0, self.height, self.cell_height):
            for x in range(0, self.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, (128, 128, 128), cell, 1)

    def next_generation(self):
        new_state = np.copy(self.game_state)

        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors = self.game_state[(x - 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y + 1) % self.n_cells_y]

                if self.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1

        self.game_state = new_state

    def draw_cells(self):
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), cell)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.width - 200 <= event.pos[0] <= self.width and self.height - 60 <= event.pos[1] <= self.height:
                    self.next_generation()
                else:
                    x, y = event.pos[0] // self.cell_width, event.pos[1] // self.cell_height
                    self.game_state[x, y] = not self.game_state[x, y]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_pause()
                elif event.key == pygame.K_s:
                    self.save_state()
                elif event.key == pygame.K_l:
                    self.load_state()

    def run_simulation(self):
        pygame.font.init()  

        while self.running:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_cells()
            self.draw_button()
            pygame.display.flip()

            self.handle_events()

            if not self.paused:
                self.next_generation()

            self.clock.tick(1 / self.tick_interval)

        pygame.quit()

if __name__ == "__main__":
    
    game = GameOfLife(800, 600, 40, 30)

    game.run_simulation()
