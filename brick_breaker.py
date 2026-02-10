import pygame
import sys

pygame.init()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 520
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

small_font = pygame.font.SysFont(None, 30)
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)


PLAY = "PLAY"
GAME_OVER = "GAME_OVER"
WIN = "WIN"
game_state = PLAY



class Paddle:
    def __init__(self):
        self.color = "White"
        self.width = 100
        self.height = 20
        self.speed = 10
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.width // 2,
            SCREEN_HEIGHT - self.height * 2,
            self.width,
            self.height
        )

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def control(self, keys):
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed


class Ball:
    def __init__(self, paddle):
        self.color = "Blue"
        self.radius = 10
        self.speed_x = 5
        self.speed_y = -5
        self.attached = True
        self.paddle = paddle
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.update_position()

    def update_position(self):
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

    def move(self):
        if self.attached:
            self.update_position()
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)



class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.life = 3
        self.color = "Green"
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update_color(self):
        if self.life == 3:
            self.color = "Green"
        elif self.life == 2:
            self.color = "Yellow"
        else:
            self.color = "Red"

    def draw(self):
        brick_life = small_font.render(f"{self.life}", True, "Black")
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(brick_life, (self.x + self.width/2 - 3, self.y))


def create_bricks():
    bricks = []
    rows = 4
    cols = 10
    padding = 10
    offset_x = 20
    offset_y = 40

    for row in range(rows):
        for col in range(cols):
            x = offset_x + col * (60 + padding)
            y = offset_y + row * (20 + padding)
            bricks.append(Brick(x, y))
    return bricks



def reset_game():
    global paddle, ball, bricks, lives, game_state
    paddle = Paddle()
    ball = Ball(paddle)
    bricks = create_bricks()
    lives = 3
    game_state = PLAY



paddle = Paddle()
ball = Ball(paddle)
bricks = create_bricks()
lives = 3


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    screen.fill("Black")

    if game_state == PLAY:
        paddle.control(keys)

        if keys[pygame.K_SPACE]:
            ball.attached = False

        ball.move()

      
        if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
            ball.speed_x *= -1
        if ball.rect.top <= 0:
            ball.speed_y *= -1

       
        if ball.rect.colliderect(paddle.rect) and ball.speed_y > 0:
            ball.speed_y *= -1
            hit_pos = (ball.rect.centerx - paddle.rect.left) / paddle.rect.width
            ball.speed_x = (hit_pos - 0.5) * 10

     
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                brick.life -= 1
                brick.update_color()
                if brick.life <= 0:
                    bricks.remove(brick)
                break

        if ball.rect.top > SCREEN_HEIGHT:
            lives -= 1
            ball.attached = True
            ball.speed_x = 5
            ball.speed_y = -5
            ball.update_position()

            if lives <= 0:
                game_state = GAME_OVER

    
        if len(bricks) == 0:
            game_state = WIN

      
        for brick in bricks:
            brick.draw()

        ball.draw()
        paddle.draw()

        lives_text = font.render(f"Lives: {lives}", True, "White")
        screen.blit(lives_text, (10, 10))

   
    elif game_state == GAME_OVER:
        text = big_font.render("GAME OVER", True, "Red")
        restart = font.render("Press R to Restart", True, "White")
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200))
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 280))

        if keys[pygame.K_r]:
            reset_game()

    
    elif game_state == WIN:
        text = big_font.render("YOU WIN", True, "Green")
        restart = font.render("Press R to Restart", True, "White")
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200))
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 280))

        if keys[pygame.K_r]:
            reset_game()

    pygame.display.flip()
    clock.tick(60)

