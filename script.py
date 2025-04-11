from turtledemo.nim import SCREENWIDTH

import pygame
import sys
import random

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17,24,47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (cur[0] + (x * GRIDSIZE), cur[1] + (y * GRIDSIZE))
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (91, 215, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (219, 83, 83)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (GRID_WIDTH-1)) * GRIDSIZE, random.randint(0,(GRID_HEIGHT-1)) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (133, 212, 180), r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (133, 212, 180), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (80, 125, 103), rr)
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT // GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH // GRIDSIZE

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food1 = Food()
    food2 = Food()

    myfont = pygame.font.SysFont("sans-serif", 25)

    score = 0
    while(True):
        clock.tick(5)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food1.position:
            snake.length += 1
            score += 1
            food1.randomize_position()
        if snake.get_head_position() == food2.position:
            snake.length += 1
            score += 1
            food2.randomize_position()
        head_x, head_y = snake.get_head_position()
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            surface.fill((255,255,255))
            game_over_text = myfont.render("Press any key to restart. Your score was: " + str(score), True, (0, 0, 0))
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            screen.blit(surface, (0, 0))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        waiting = False

            snake = Snake()
            food1 = Food()
            food2 = Food()
            score = 0
            continue
        snake.draw(surface)
        food1.draw(surface)
        food2.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("score: " + str(score), 1, (255,255,255))
        screen.blit(text, (5,10))
        pygame.display.update()

main()