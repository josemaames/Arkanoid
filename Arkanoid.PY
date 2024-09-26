import pygame
from config import Config
from user_management import authenticate_user  # Importar la función para autenticación
from score_management import save_score, get_high_scores  # Importar funciones de gestión de puntuaciones

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, Config.BRICK_WIDTH, Config.BRICK_HEIGHT)
        self.hit = False

def draw_paddle(screen, x):
    paddle_rect = pygame.Rect(x, Config.SCREEN_HEIGHT - Config.PADDLE_HEIGHT, Config.PADDLE_WIDTH, Config.PADDLE_HEIGHT)
    pygame.draw.rect(screen, (0, 255, 0), paddle_rect)
    return paddle_rect

def draw_ball(screen, x, y):
    ball_rect = pygame.Rect(x, y, Config.BALL_SIZE, Config.BALL_SIZE)
    pygame.draw.ellipse(screen, (0, 0, 255), ball_rect)
    return ball_rect

def draw_bricks(screen, bricks):
    for brick in bricks:
        if not brick.hit:
            pygame.draw.rect(screen, Config.BRICK_COLOR, brick.rect)

def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def main():
    pygame.init()
    
    # Autenticación de usuario (puedes cambiar esto para hacerlo interactivo)
    username = "Alexander"  # Cambia esto según sea necesario
    password = "Peñaloza"  # Cambia esto según sea necesario
    user = authenticate_user(username, password)
    if not user:
        print("Usuario no autenticado. Saliendo...")
        return

    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Arkanoid Game")
    
    paddle_x = (Config.SCREEN_WIDTH - Config.PADDLE_WIDTH) // 2
    ball_x = Config.SCREEN_WIDTH // 2
    ball_y = Config.SCREEN_HEIGHT // 2
    ball_speed_x = Config.BALL_SPEED_X
    ball_speed_y = Config.BALL_SPEED_Y

    # Crear los ladrillos
    bricks = []
    for row in range(Config.BRICK_ROWS):
        for col in range(Config.BRICK_COLUMNS):
            brick_x = col * (Config.BRICK_WIDTH + 10) + 10
            brick_y = row * (Config.BRICK_HEIGHT + 5) + 30
            bricks.append(Brick(brick_x, brick_y))

    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Mover la pala
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 5
        if keys[pygame.K_RIGHT] and paddle_x < Config.SCREEN_WIDTH - Config.PADDLE_WIDTH:
            paddle_x += 5
        
        # Actualizar la posición de la pelota
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisiones de la pelota con los bordes
        if ball_x <= 0 or ball_x >= Config.SCREEN_WIDTH - Config.BALL_SIZE:
            ball_speed_x *= -1
        if ball_y <= 0:
            ball_speed_y *= -1
        
        # Verifica si la bola cae
        if ball_y >= Config.SCREEN_HEIGHT - Config.BALL_SIZE:
            print("¡Perdiste!")
            save_score(username, score)  # Guarda el score en la base de datos
            score = 0  # Resetea el puntaje a 0
            ball_x = Config.SCREEN_WIDTH // 2  # Reinicia la posición de la bola
            ball_y = Config.SCREEN_HEIGHT // 2  # Reinicia la posición de la bola
            continue  # Vuelve al inicio del ciclo para resetear el juego

        # Colisión de la pelota con la pala
        paddle_rect = draw_paddle(screen, paddle_x)
        ball_rect = draw_ball(screen, ball_x, ball_y)
        if ball_rect.colliderect(paddle_rect):
            ball_speed_y *= -1

        # Comprobar colisiones con ladrillos
        for brick in bricks:
            if not brick.hit and ball_rect.colliderect(brick.rect):
                brick.hit = True
                ball_speed_y *= -1
                score += 10
                break

        # Limpiar pantalla y dibujar elementos
        screen.fill((0, 0, 0))  # Limpia la pantalla con un fondo negro
        draw_bricks(screen, bricks)
        draw_paddle(screen, paddle_x)
        draw_ball(screen, ball_x, ball_y)
        draw_score(screen, score)

        pygame.display.flip()  # Actualiza la pantalla
        pygame.time.delay(30)  # Añade un pequeño retraso

    pygame.quit()

if __name__ == "__main__":
    main()
