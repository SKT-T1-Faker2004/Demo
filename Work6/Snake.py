import random
import pygame


class Point():
    row = 0
    clo = 0

    def __init__(self, row, clo):
        self.row = row
        self.clo = clo

    def copy(self):
        return Point(row=self.row, clo=self.clo)


pygame.init()
width = 800
hight = 400

ROW = 30
CLO = 40

direct = 'left'
window = pygame.display.set_mode((width, hight))
pygame.display.set_caption('贪吃蛇 By EricZ')

head = Point(row=int(ROW / 2), clo=int(CLO / 2))

snake = [
    Point(row=head.row, clo=head.clo + 1),
    Point(row=head.row, clo=head.clo + 2),
    Point(row=head.row, clo=head.clo + 3)

]


def gen_food():
    while True:
        position = Point(row=random.randint(0, ROW - 1),
                         clo=random.randint(0, CLO - 1))
        is_coll = False
        if head.row == position.row and head.clo == position.clo:
            is_coll = True
        for body in snake:
            if body.row == position.row and head.row == position.row:
                is_coll = True
                break
        if not is_coll:
            break
    return position


head_color = (0, 158, 128)

snakeFood = gen_food()

snakeFood_color = (255, 255, 0)

snake_color = (200, 147, 158)


def rect(point, color):
    left = point.clo * width / CLO
    top = point.row * hight / ROW

    pygame.draw.rect(window, color, (left, top, width / CLO, hight / ROW))


quit = True
clock = pygame.time.Clock()

while quit:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 273 or event.key == 119:
                if direct == 'left' or direct == 'right':
                    direct = 'top'

            if event.key == 274 or event.key == 115:
                if direct == 'left' or direct == 'right':
                    direct = 'bottom'

            if event.key == 276 or event.key == 97:
                if direct == 'top' or direct == 'bottom':
                    direct = 'left'

            if event.key == 275 or event.key == 100:
                if direct == 'top' or direct == 'bottom':
                    direct = 'right'

    eat = (head.row == snakeFood.row and head.clo == snakeFood.clo)

    if eat:
        snakeFood = Point(row=random.randint(0, ROW - 1),
                          clo=random.randint(0, CLO - 1))
    snake.insert(0, head.copy())
    if not eat:
        snake.pop()

    if direct == 'left':
        head.clo -= 1
    if direct == 'right':
        head.clo += 1
    if direct == 'top':
        head.row -= 1
    if direct == 'bottom':
        head.row += 1

    dead = False
    if head.clo < 0 or head.row < 0 or head.clo >= CLO or head.row >= ROW:
        dead = True
    for body in snake:
        if head.clo == body.clo and head.row == body.row:
            dead = True
            break
    if dead:
        print('Game Over')
        quit = False

    pygame.draw.rect(window, (245, 135, 155), (0, 0, width, hight))

    rect(head, head_color)
    rect(snakeFood, snakeFood_color)

    for body in snake:
        rect(body, snake_color)

    pygame.display.flip()
