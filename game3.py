import pgzrun
import random

TITLE = "Arkanoid clone"
WIDTH = 800
HEIGHT = 500

paddle = Actor("paddleblue.png")
paddle.x = 120
paddle.y = 420

ball = Actor("ballblue.png")
ball.x = 100
ball.y = 300

ball_x_speed = -3
ball_y_speed = -3

bars_list = []
score = 0
game_over = False
game_won = False

def draw():
    screen.blit("background.png", (0,0))
    paddle.draw()
    ball.draw()
    
    for bar in bars_list:
        bar.draw()
    
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
    
    if game_over:
        screen.draw.text("Perdiste", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="red")
    elif game_won:
        screen.draw.text("Ganaste", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="green")

def place_bars(x,y,image):
    bar_x = x
    bar_y = y
    for i in range(8):
        bar = Actor(image)
        bar.x = bar_x
        bar.y = bar_y
        bar_x += 70
        bars_list.append(bar)

def update():
    global ball_x_speed, ball_y_speed, score, game_over, game_won
    
    if not game_over and not game_won:
        if keyboard.left and paddle.x > 0:
            paddle.x = paddle.x - 5
        if keyboard.right and paddle.x < WIDTH:
            paddle.x = paddle.x + 5

        update_ball()

        for bar in bars_list:
            if ball.colliderect(bar):
                bars_list.remove(bar)
                ball_y_speed *= -1
                score += 10

        if paddle.colliderect(ball):
            ball_y_speed *= -1
            handle_paddle_collision()

        # Check if all blocks are cleared
        if len(bars_list) == 0:
            game_won = True

def handle_paddle_collision():
    global ball_x_speed, ball_y_speed
    
    # Adjust the ball's direction based on where it hits the paddle
    offset = ball.x - paddle.x
    offset_percentage = offset / paddle.width  # percentage of where the ball hits
    
    # Change ball_x_speed based on the hit position
    ball_x_speed = 6 * offset_percentage
    ball_y_speed = -abs(ball_y_speed)  # Make sure the ball goes upward after hitting the paddle
    
    # Slightly increase speed after each paddle hit
    ball_x_speed *= 1.05
    ball_y_speed *= 1.05

def update_ball():
    global ball_x_speed, ball_y_speed, game_over
    ball.x += ball_x_speed
    ball.y += ball_y_speed
    
    if ball.x >= WIDTH or ball.x <= 0:
        ball_x_speed *= -1
    if ball.y <= 0:
        ball_y_speed *= -1

    # If the ball falls below the paddle
    if ball.y >= HEIGHT:
        game_over = True

coloured_box_list = ["element_blue_rectangle_glossy.png", "element_green_rectangle_glossy.png","element_red_rectangle_glossy.png"]
x = 120
y = 100
for coloured_box in coloured_box_list:
    place_bars(x, y, coloured_box)
    y += 50

pgzrun.go()


