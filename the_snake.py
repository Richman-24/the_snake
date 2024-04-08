from random import randint
from typing import Tuple

import pygame

# Константы для размеров поля и сетки:
BORDER = 20 
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480 #Длина и ширина игрового поля
GRID_SIZE = 20 #Размер ячейки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE #Количество ячеек по горизонтали
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE #Количество ячеек по вертикали

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#Цветовая схема
BOARD_BACKGROUND_COLOR = (0, 0, 0) # Цвет фона - черный:
BORDER_COLOR = (93, 216, 228) # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0) # Цвет яблока
SNAKE_COLOR = (0, 255, 0) # Цвет змейки
BORDER_COLOR = (255, 255, 255)
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32) #Настрйока экрана
pygame.display.set_caption('Змейка') # Заголовок окна игрового окна:

# Настройка времени:
clock = pygame.time.Clock()
SPEED = 10 # Частота обновления кадров:

# Настройка игрового события - обновлять каждые 200 мс
GAME_EVENT = pygame.USEREVENT #создание пользовательского типа события (обновление поля)
pygame.time.set_timer(GAME_EVENT, 200) #скорость обновления игровых событий - 5 раз\сек



# Тут опишите все классы игры.
class GameObject:

    def __init__(self) -> None:
        self.position = ...
        self.body_color = ...
        self.score = 0

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

    def rand_position(self): 

        _x = randint(0, GRID_WIDTH-1)
        _y = randint(0, GRID_HEIGHT-1)
        
        return (_x, _y) #Создаёт новую позицию для яблока (если скушан фрукт)
    
class Snake(GameObject):

    def __init__(self) -> None:
        super().__init__()
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.check_eated = False
    
    def draw(self):  # рисует змейку в данный момент на доске
        for tile in self.positions:
            rect = (pygame.Rect(self.formating_coord(tile), (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


    def snake_step(self):  # изменяет положение змейки на 1 по направлению движения
        self.positions.insert(0, (self.positions[0][0] + self.direction[0],
                                    self.positions[0][1] + self.direction[1]))
        if self.check_eated:
            self.check_eated = False
        else: 
            self.positions.pop()

    def reset(self):
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = RIGHT

class GameLogic:
    '''Класс содержит логику игры и работает с классами Snake и Apple'''
    
    def __init__(self) -> None:
        self.snake = Snake()
        self.apple = Apple()
        self.score = 0

    #Затираем экран и заново отрисовываем всё поле
    def draw(self):
        self.snake.draw()
        self.apple.draw()

    #Обрабатываем обновление игрового события
    def game_event(self):
        self.snake.snake_step()
        self.apple_collision()
        self.self_collision()
        self.wall_collision()
        

    # если позиция головы змейки совпадает с позицией еды - увеличивается на 1 тайл
    def apple_collision(self):  
        if self.snake.positions[0] == self.apple.position:
            self.apple.position = self.apple.rand_position()
            self.snake.check_eated = True
            self.score += 10

    # Описание поведения при выходе за границу игрового поля
    def wall_collision(self): 
        for index, position in enumerate(self.snake.positions):
            if position[0] > GRID_WIDTH-1: # x, y x>32 = (0, y)
                self.snake.positions[index] = (0, position[1])
            if position[0] < 0: # x, y x<0 = (32, y)
                self.snake.positions[index] = (GRID_WIDTH-1, position[1])
            if position[1] > GRID_HEIGHT-1:
                self.snake.positions[index] = (position[0], 0) 
            if position[1] < 0:
                self.snake.positions[index] = ((position[0], GRID_HEIGHT-1)) 
    
    #Проверка если голова змейки == любой тайл змейки = смерть
    def self_collision(self): 
        if self.snake.positions[0] in self.snake.positions[1:]:
            self.snake.reset()
            self.score = 0    

def main():
    pygame.init()
    SCORE_FONT = pygame.font.Font(None, 20)

    game = GameLogic()
    
    
    while True:
        clock.tick(SPEED)

        for event in pygame.event.get():
            if event.type == GAME_EVENT:
                game.game_event()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction != DOWN:
                    game.snake.direction = UP
                elif event.key == pygame.K_DOWN and game.snake.direction != UP:
                    game.snake.direction = DOWN
                elif event.key == pygame.K_LEFT and game.snake.direction != RIGHT:
                    game.snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and game.snake.direction != LEFT:
                    game.snake.direction = RIGHT
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        screen.fill(BOARD_BACKGROUND_COLOR)
        game.draw()
        screen.blit(SCORE_FONT.render(f"Очки охоты: {game.score}",
                                     True, BORDER_COLOR), (25, 25))
        
        pygame.display.update()

if __name__ == '__main__':
    main()
