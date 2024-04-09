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


class GameObject:
    """Класс определяет игровые сущности"""

    SCORE = 0

    def __init__(self) -> None:
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Рисует игровую сущность"""
        pass

    @staticmethod
    def formating_coord(coordinate: Tuple[int, int]) -> Tuple[int, int]:
        """Переводит координаты из формата абсолютного в формат ячеек"""
        return (coordinate[0] * GRID_SIZE, coordinate[1] * GRID_SIZE)

    @staticmethod
    def randomize_position():  # Можно же создавать не только яблоко
        """Создаёт новую случайную позицию для клетки на карте"""
        _x = randint(0, GRID_WIDTH - 1)
        _y = randint(0, GRID_HEIGHT - 1)

        return (_x, _y)

    @classmethod
    def auto_dificult(cls):
        """Меняет сложность в зависимости от набранных очков"""
        global SCORE
        if cls.SCORE >= 150:
            pygame.time.set_timer(GAME_EVENT, 25)
        elif cls.SCORE >= 100:
            pygame.time.set_timer(GAME_EVENT, 50)
        elif cls.SCORE >= 50:
            pygame.time.set_timer(GAME_EVENT, 100)


class Apple(GameObject):
    """Класс определяет поведение яблока"""

    def __init__(self) -> None:
        super().__init__()

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
        self.last = (0, 0)

    def draw(self):
        """рисует змейку в данный момент на доске"""
        for tile in self.positions:
            rect = pygame.Rect(
                self.formating_coord(tile), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """изменяет положение змейки на 1 по направлению движения"""
        self.positions.insert(
            0,
            (
                (self.positions[0][0] + self.direction[0]) % GRID_WIDTH,
                (self.positions[0][1] + self.direction[1]) % GRID_HEIGHT,
            ),
        )
        if self.check_eated:
            self.check_eated = False
        else:
            self.last = self.formating_coord(
                self.positions.pop()
            )

    def get_head_position(self):
        """Возвращает позицию головы змеи"""
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

    def apple_collision(self, apple):
        """определяет поведение при совпадении головы змеи и яблока"""
        if self.positions[0] == apple.position:
            while apple.position in self.positions:
                apple.position = apple.randomize_position()
            self.check_eated = True
            GameObject.SCORE += 10

    def self_collision(self):
        """Проверка если голова змейки ест сама себя"""
        if self.positions[0] in self.positions[1:]:
            self.reset()
            super().SCORE = 0
            pygame.time.set_timer(GAME_EVENT, 200)


def handle_keys(snake, event):
    """Определяет реакцию на нажатие клавиш"""
    binded_keys = {
        pygame.K_UP: UP if snake.direction != DOWN else DOWN,
        pygame.K_DOWN: DOWN if snake.direction != UP else UP,
        pygame.K_RIGHT: RIGHT if snake.direction != LEFT else LEFT,
        pygame.K_LEFT: LEFT if snake.direction != RIGHT else RIGHT,
    }

    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        snake.next_direction = binded_keys.get(event.key)


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
                snake.apple_collision(apple)
                snake.self_collision()
                snake.auto_dificult()

            handle_keys(snake, event)

        snake.draw()
        apple.draw()
        screen.blit(
            SCORE_FONT.render(
                f"Очки охоты: {snake.SCORE}", True,
                BORDER_COLOR, BOARD_BACKGROUND_COLOR), (25, 25)
        )

        pygame.display.update()


if __name__ == "__main__":
    main()
