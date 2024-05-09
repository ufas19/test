import random

class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]

    def draw(self):
        print('+' + '-' * self.width + '+')

        for row in self.grid:
            print('|' + ''.join(row) + '|')

        print('+' + '-' * self.width + '+')

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 'UP'

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def shoot(self):
        return Bullet(self.x, self.y, self.direction)

    def get_direction_symbol(self):
        if self.direction == 'UP':
            return '^'
        elif self.direction == 'DOWN':
            return 'v'
        elif self.direction == 'LEFT':
            return '<'
        elif self.direction == 'RIGHT':
            return '>'

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self):
        if self.direction == 'UP':
            self.y -= 1
        elif self.direction == 'DOWN':
            self.y += 1
        elif self.direction == 'LEFT':
            self.x -= 1
        elif self.direction == 'RIGHT':
            self.x += 1

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def hit(self, bullet):
        return self.x == bullet.x and self.y == bullet.y

    def move_to_random_location(self, field_width, field_height):
        self.x = random.randint(0, field_width - 1)
        self.y = random.randint(0, field_height - 1)

class Game:
    def __init__(self, width, height):
        self.field = Field(width, height)
        self.tank = Tank(random.randint(0, width-1), random.randint(0, height-1))
        self.bullets = []
        self.target = Target(random.randint(0, width-1), random.randint(0, height-1))
        self.score = 0

    def is_valid_move(self, x, y):
        return 0 <= x < self.field.width and 0 <= y < self.field.height

    def update_target(self):
        if any(self.target.hit(bullet) for bullet in self.bullets):
            print("Target hit!")
            self.score += 1
            self.target.move_to_random_location(self.field.width, self.field.height)

    def remove_bullets(self):
        for bullet in self.bullets[:]:
            if not self.is_valid_move(bullet.x, bullet.y):
                self.bullets.remove(bullet)

    def play(self):
        while True:
            self.field.grid = [[' ' for _ in range(self.field.width)] for _ in range(self.field.height)]
            self.remove_bullets()
            self.update_target()

            for bullet in self.bullets[:]:
                bullet.move()
                if self.is_valid_move(bullet.x, bullet.y):
                    self.field.grid[bullet.y][bullet.x] = '*'
                else:
                    self.bullets.remove(bullet)

            if self.is_valid_move(self.tank.x, self.tank.y):
                self.field.grid[self.tank.y][self.tank.x] = 'T'
                self.field.grid[self.tank.y][self.tank.x] = self.tank.get_direction_symbol()

            if self.is_valid_move(self.target.x, self.target.y):
                self.field.grid[self.target.y][self.target.x] = 'X'

            self.field.draw()
            print("Score:", self.score)

            action = input("Action (W/A/S/D to move, SPACE to shoot): ").upper()

            if action == 'W':
                if self.is_valid_move(self.tank.x, self.tank.y - 1):
                    self.tank.move(0, -1)
                    self.tank.direction = 'UP'
            elif action == 'A':
                if self.is_valid_move(self.tank.x - 1, self.tank.y):
                    self.tank.move(-1, 0)
                    self.tank.direction = 'LEFT'
            elif action == 'S':
                if self.is_valid_move(self.tank.x, self.tank.y + 1):
                    self.tank.move(0, 1)
                    self.tank.direction = 'DOWN'
            elif action == 'D':
                if self.is_valid_move(self.tank.x + 1, self.tank.y):
                    self.tank.move(1, 0)
                    self.tank.direction = 'RIGHT'
            elif action == ' ':
                self.bullets.append(self.tank.shoot())

if __name__ == "__main__":
    game = Game(20, 10)
    game.play()
