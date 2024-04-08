from random import randint
from typing import Tuple

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Длина и ширина игрового поля
GRID_SIZE = 20  # Размер ячейки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Количество ячеек по горизонтали
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Количество ячеек по вертикали

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цветовая схема
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный:
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки
BORDER_COLOR = (255, 255, 255)

# Настройка игрового окна:
screen = pygame.display.set_mode(  # Настройка экрана
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)
pygame.display.set_caption("Змейка")  # Заголовок окна игрового окна:

# Настройка времени:
clock = pygame.time.Clock()
SPEED = 30  # Частота обновления кадров FPS:

GAME_EVENT = pygame.USEREVENT  # создание пользовательского типа события
pygame.time.set_timer(
    GAME_EVENT, 200
)  # скорость обновления игровых событий - 5 раз\сек

SCORE = 0  # Счётчик отчков, вличяет на сложность


class GameObject:
    """Класс определяет игровые сущности"""

    def __init__(self) -> None:
        self.position = (0, 0)
        self.body_color = (255, 255, 255)
        self.SCORE = 0

    def draw(self):
        """Рисует игровую сущность"""
        pass

    @staticmethod
    def formating_coord(coordinate: Tuple[int, int]) -> Tuple[int, int]:
        """Переводит координаты из формата абсолютного в формат ячеек"""
        return (coordinate[0] * GRID_SIZE, coordinate[1] * GRID_SIZE)


class Apple(GameObject):
    """Класс определяет поведение яблока"""

    def __init__(self) -> None:
        super().__init__()
        # self.snake = snake
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Создаёт новую случайную позицию для яблока (если скушан фрукт)"""
        _x = randint(0, GRID_WIDTH - 1)
        _y = randint(0, GRID_HEIGHT - 1)

        return (_x, _y)

    def draw(self):
        """Рисует яблоко на доске"""
        rect = pygame.Rect(
            self.formating_coord(self.position), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс определяет поведение змеи"""

    def __init__(self) -> None:
        super().__init__()
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.check_eated = False
        self.next_direction = None

    def draw(self):
        """рисует змейку в данный момент на доске"""
        for tile in self.positions:
            rect = pygame.Rect(
                self.formating_coord(tile), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """изменяет положение змейки на 1 по направлению движения"""
        self.positions.insert(
            0,
            (
                self.positions[0][0] + self.direction[0],
                self.positions[0][1] + self.direction[1],
            ),
        )
        if self.check_eated:
            self.check_eated = False
        else:
            self.positions.pop()

    def get_head_position(self):
        """возвращает позицию головы змеи"""
        return self.positions[0]

    def reset(self):
        """Обновляет состояние змейки после фейла"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT

    def update_direction(self):
        """Обновляет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake, event):
    """Определяет реакцию на нажатие клавиш"""
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and snake.direction != DOWN:
            snake.next_direction = UP
        elif event.key == pygame.K_DOWN and snake.direction != UP:
            snake.next_direction = DOWN
        elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
            snake.next_direction = LEFT
        elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
            snake.next_direction = RIGHT

        elif event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))


def auto_dificult():
    """Изменение сложности игры в зависимости от очков охоты"""
    global SCORE
    """Меняет сложность в зависимости от набранных очков"""
    if SCORE >= 150:
        pygame.time.set_timer(GAME_EVENT, 25)
    elif SCORE >= 100:
        pygame.time.set_timer(GAME_EVENT, 50)
    elif SCORE >= 50:
        pygame.time.set_timer(GAME_EVENT, 100)


def wall_collision(snake):
    """Описание поведения при выходе за границу игрового поля"""
    for index, position in enumerate(snake.positions):
        if position[0] > GRID_WIDTH - 1:
            snake.positions[index] = (0, position[1])
        if position[0] < 0:
            snake.positions[index] = (GRID_WIDTH - 1, position[1])
        if position[1] > GRID_HEIGHT - 1:
            snake.positions[index] = (position[0], 0)
        if position[1] < 0:
            snake.positions[index] = (position[0], GRID_HEIGHT - 1)


def apple_collision(snake, apple):
    """определяет поведение при совпадении головы змеи и яблока"""
    global SCORE
    if snake.positions[0] == apple.position:
        while apple.position in snake.positions:
            apple.position = apple.randomize_position()
        snake.check_eated = True
        SCORE += 10


def self_collision(snake):
    """Проверка если голова змейки ест сама себя"""
    global SCORE
    if snake.positions[0] in snake.positions[1:]:
        snake.reset()
        SCORE = 0
        pygame.time.set_timer(GAME_EVENT, 200)


def main():
    """Основная логика игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    SCORE_FONT = pygame.font.Font(None, 20)

    while True:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == GAME_EVENT:
                snake.update_direction()
                snake.move()
                apple_collision(snake, apple)
                self_collision(snake)
                wall_collision(snake)
                auto_dificult()

            handle_keys(snake, event)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        screen.blit(
            SCORE_FONT.render(
                f"Очки охоты: {SCORE}", True, BORDER_COLOR), (25, 25)
        )

        pygame.display.update()


if __name__ == "__main__":
    main()
