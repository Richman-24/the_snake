﻿from random import choice, randint

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:

    def __init__(self) -> None:
        pass

    def draw(self):
        pass

class Apple(GameObject):

    def __init__(self) -> None:
        super().__init__()

    def draw(self): ... # рисует змейку в данный момент на доске

    def rand_position(self): ... #Создаёт новую позицию для яблока (если скушан фрукт)

class Snake(GameObject):

    def __init__(self) -> None:
        super().__init__()

    def draw(self): ... # рисует змейку в данный момент на доске

    def move(self): ... # изменяет положение змейки на 1 по направлению движения

    def eat(self): ... # если позиция головы змейки совпадает с позицией еды - увеличивается на 1 тайл

    def die(self): ... # Если змейка достигает есть себя (self_collision) - игра окончена
    
    def wall_collision(self): ... # Проверка если тайд змейки вышел за границу поля -> отразить её с другой стороны

    def self_collision(self): ... #Проверка если голова змейки == тайл змейки = смерть

    def handle_keys(game_object): # Функция обработки действий пользователя
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif event.key == pygame.K_DOWN and game_object.direction != UP:
                    game_object.next_direction = DOWN
                elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                    game_object.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                    game_object.next_direction = RIGHT

    def update_direction(self): # Метод обновления направления после нажатия на кнопку
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():

    snake = Snake()
    apple = Apple()
    
    ...

    while True:
        clock.tick(SPEED)

        snake.draw()
        apple.draw()

        snake.handle_keys()

        pygame.display.update()


if __name__ == '__main__':
    main()