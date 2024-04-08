from random import choice, randint
from typing import Tuple

import pygame

# Инициализация PyGame:


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

# Частота обновления кадров:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Настройка игрового события - обновлять каждые 200 мс
GAME_EVENT = pygame.USEREVENT
pygame.time.set_timer(GAME_EVENT, 200) #скорость обновления игровых событий 500\1000 

# Тут опишите все классы игры.
class GameObject:

    def __init__(self) -> None:
        self.position = ...
        self.body_color = ...

    def draw(self):
        rect = pygame.Rect(self.formating_coord(self.position), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def formating_coord(coordinate: Tuple[int, int]) -> Tuple[int, int]:
        return (coordinate[0]*GRID_SIZE, coordinate[1]*GRID_SIZE)
    

class Apple(GameObject):

    def __init__(self) -> None:
        super().__init__()
        self.position = self.rand_position()
        self.body_color = APPLE_COLOR

    #def draw(self): ... # рисует Яблоко в данный момент на доске

    def rand_position(self): 

        print('Randoming apple...')

        _x = randint(0, GRID_WIDTH-1)
        _y = randint(0, GRID_HEIGHT-1)
        
        return (_x, _y) #Создаёт новую позицию для яблока (если скушан фрукт)

class Snake(GameObject):

    def __init__(self) -> None:
        super().__init__()
        self.positions = [(0, 0)]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.check_eated = False
    
    def draw(self):  # рисует змейку в данный момент на доске
        for tile in self.positions:
            rect = (pygame.Rect(self.formating_coord(tile), (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


    def move(self):  # изменяет положение змейки на 1 по направлению движения
        self.positions.insert(0, (self.positions[0][0] + self.direction[0],
                                    self.positions[0][1] + self.direction[1]))
        if self.check_eated:
            self.check_eated = False
        else: 
            self.positions.pop()


    
    
class GameLogic:
    
    '''Класс содержит логику игры и работает с классами Snake и Apple'''
    def __init__(self) -> None:
        self.snake = Snake()
        self.apple = Apple()

    #затираем экран и заново отрисовываем всё поле
    def draw(self):
        
        print(f'{self.snake.positions} - {self.apple.position}')

        screen.fill(BOARD_BACKGROUND_COLOR)
        self.snake.draw()
        self.apple.draw()

    def game_event(self):
        self.check_eat()
        self.snake.move()
        

    # если позиция головы змейки совпадает с позицией еды - увеличивается на 1 тайл
    def check_eat(self):  
        if self.snake.positions[0] == self.apple.position:
            self.snake.check_eaten = True
            self.apple.position = self.apple.rand_position()

    # Проверка если тайд змейки вышел за границу поля -> отразить её с другой стороны
    def wall_collision(self): ... 
    
    #Проверка если голова змейки == любой тайл змейки = смерть
    def self_collision(self): 
        if self.snake.positions[0] in self.snake.positions[1:]:
            self.game_over()

    # Если self_collision Сообщение о конце игры
    def game_over(self): 
        print(f"Игра окончена")
        
    
    def handle_keys(self): # Функция обработки действий пользователя
        for event in pygame.event.get():
            if event.type == GAME_EVENT:
                self.game_event()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.direction = RIGHT
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

def main():
    pygame.init()
    game = GameLogic()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        game.draw()
        game.handle_keys()
        
        pygame.display.update()

if __name__ == '__main__':
    main()
