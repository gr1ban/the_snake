from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
     """Базовый класс игры""" 
    def __init__ (self):
        """Конструктор базового класса игры"""
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = None

    def draw(self, surface):
        """Метод отрисовки на экране"""
        pass    
class Apple(GameObject):
    """Дочерний класс яблоко"""
    def __init__(self):
        """Конструктор дочернего класс яблоко"""
        self.body_color = (255, 0, 0)
        self.position = self.randomize_position()

    def draw(self, surface):
        """Метод отрисовки на экране"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)    

    def randomize_position(self):
        """Метод появления яблока"""
        return (randint(0, GRID_WIDTH-1) * GRID_SIZE, randint(0, GRID_HEIGHT-1) * GRID_SIZE)


class Snake(GameObject):
    """Дочерний класс змея"""
    def __init__(self):
        """Конструктор дочернего класса змея"""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = []
        self.positions.append(self.position)
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Метод изменения движения при нажатии клавиатуры"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обработки движения змеи"""
        head_position = self.get_head_position()
        new_position = ()
        if self.direction == RIGHT:
            new_position = (head_position[0] + (RIGHT[0] * GRID_SIZE), head_position[1] + (RIGHT[1] * GRID_SIZE))
        elif self.direction == LEFT:
            new_position = (head_position[0] + (LEFT[0] * GRID_SIZE), head_position[1] + (LEFT[1] * GRID_SIZE))
        elif self.direction == UP:
            new_position = (head_position[0] + (UP[0] * GRID_SIZE), head_position[1] + (UP[1] * GRID_SIZE))
        elif self.direction == DOWN:
            new_position = (head_position[0] + (DOWN[0] * GRID_SIZE), head_position[1] + (DOWN[1] * GRID_SIZE))
        else:
            new_position = (head_position[0] + GRID_SIZE, head_position[1])

        if new_position[0] > (SCREEN_WIDTH - 20):
            new_position = (0, head_position[1])
        if new_position[1] > (SCREEN_HEIGHT - 20):
            new_position = (head_position[0], 0)
        if new_position[0] < 0:
            new_position = (SCREEN_WIDTH - 20, head_position[1])
        if new_position[1] < 0:
            new_position = (head_position[0], SCREEN_HEIGHT - 20)

        if new_position in self.positions[1:-1]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop(-1)

    def draw(self, surface):
        """Метод отрисовки змеи"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод передачи координат головы"""
        return self.positions[0]

    def reset(self):
        """Метод обнуление игры при столкновении"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None


def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if (apple.position in snake.positions):
            snake.length += 1
            apple = Apple()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


def handle_keys(game_object):
    """Обработка нажатие на клавиатуре"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
        

if __name__ == '__main__':
    main()