import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre du jeu
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong Game")

# Couleurs
green = (152, 251, 152)  # Couleur de fond (vert menthe)
dark_green = (34, 139, 34)  # Vert foncé
red = (255, 0, 0)  # Rouge
blue = (0, 0, 255)  # Bleu
black = (0, 0, 0)   # noir
white = (255, 255, 255) # blanc

# Variables du jeu
player_score = 0
opponent_score = 0
max_score = 3
game_over = False
winner = ""

ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
player = pygame.Rect(width - 20, height // 2 - 70, 10, 140)
opponent = pygame.Rect(10, height // 2 - 70, 10, 140)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Font
font = pygame.font.Font(None, 64)

# Fonction pour redémarrer le jeu
def restart_game():
    global game_over, player_score, opponent_score, ball_speed_x, ball_speed_y, player_speed, opponent_speed
    player_score = 0
    opponent_score = 0
    game_over = False
    ball.center = (width // 2, height // 2)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    player_speed = 0
    opponent_speed = 7

# Fonction pour afficher le score
def display_score():
    player_text = font.render(str(player_score), True, dark_green)
    opponent_text = font.render(str(opponent_score), True, red)
    screen.blit(player_text, (width // 2 + 30, 10))
    screen.blit(opponent_text, (width // 2 - 50, 10))

# Fonction principale du jeu
def main():
    global game_over, player_score, opponent_score, ball_speed_x, ball_speed_y, player_speed, opponent_speed, winner

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7
        
        # Mouvement du joueur
        player.y += player_speed
        if player.top <= 0:
            player.top = 0
        if player.bottom >= height:
            player.bottom = height

        # Mouvement de l'adversaire automatique (IA)
        if opponent.top < ball.y:
            opponent.top += opponent_speed
        if opponent.bottom > ball.y:
            opponent.bottom -= opponent_speed

        # Mouvement de la balle
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Rebond de la balle (collision avec les murs)
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        # Rebond de la balle (collision avec les raquettes)
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

        # Gestion des scores
        if ball.left <= 0:
            player_score += 1
            if player_score == max_score:
                game_over = True
                winner = "You Win!"
            else:
                ball_speed_x *= random.choice((1, -1))
                ball_speed_y *= random.choice((1, -1))
                ball.center = (width // 2, height // 2)
        
        if ball.right >= width:
            opponent_score += 1
            if opponent_score == max_score:
                game_over = True
                winner = "Elena Win"
            else:
                ball_speed_x *= random.choice((1, -1))
                ball_speed_y *= random.choice((1, -1))
                ball.center = (width // 2, height // 2)

        # Fond du terrain
        screen.fill(green)
        
        # Affichage des raquettes, de la balle et du score
        pygame.draw.rect(screen, dark_green, player)
        pygame.draw.rect(screen, red, opponent)
        pygame.draw.ellipse(screen, (255, 255, 0), ball)
        display_score()

        # Affichage du bouton Restart et du message du gagnant
        if game_over:
            display_score()
            restart_button = pygame.Rect(width // 2 - 100, height - 50, 200, 40)
            pygame.draw.rect(screen, blue, restart_button)
            restart_text = font.render("Restart", True, black)
            # Création du bouton arrondi
            button_width, button_height = restart_text.get_width() + 20, restart_text.get_height() + 10
            button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, white, (0, 0, button_width, button_height), border_radius=10)

            # Placement du texte au centre du bouton
            text_x = (button_width - restart_text.get_width()) // 2
            text_y = (button_height - restart_text.get_height()) // 2
            button_surface.blit(restart_text, (text_x, text_y))
            # Affichage du bouton sur l'écran
            screen.blit(button_surface, (width // 2 - button_width // 2, height - 60))
            winner_text = font.render(winner, True, dark_green if winner == "You Win!" else red)
            screen.blit(winner_text, (width // 2 - 100, height // 2 - 100))
            
            # Arrêter tous les mouvements
            ball_speed_x, ball_speed_y, player_speed, opponent_speed = 0, 0, 0, 0 

        # Mise à jour de l'affichage
        pygame.display.flip()
        clock.tick(60)

        # Logique pour redémarrer le jeu
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_x, mouse_y):
                        restart_game()

    pygame.quit()

# Démarrer le jeu
restart_game()
main()
