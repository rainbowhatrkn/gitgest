import pygame
import sys
import subprocess
from pygame.locals import QUIT, MOUSEBUTTONDOWN, VIDEORESIZE, KEYDOWN

# Initialisation de Pygame
pygame.init()

# Définir les couleurs
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARK_GREY = (40, 40, 40)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
# Dimensions initiales de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Configuration de la fenêtre
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Git Command Center")

# Fontes
font = pygame.font.SysFont('Courier', 24)
small_font = pygame.font.SysFont('Courier', 18)

# Fonction pour dessiner les boutons
def draw_button(surface, text, rect, color):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (rect.x + 10, rect.y + 10))

# Fonction pour dessiner une zone de texte
def draw_text_box(surface, text, rect):
    pygame.draw.rect(surface, WHITE, rect, 2)
    text_surface = font.render(text, True, WHITE)
    surface.blit(text_surface, (rect.x + 5, rect.y + 5))

# Fonction pour exécuter des commandes Git et afficher la sortie
def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

# Fonction pour gérer les clics sur les boutons
def handle_button_click(position, rects):
    for i, rect in enumerate(rects):
        if rect.collidepoint(position):
            return i
    return None

# Configuration des boutons et autres éléments
button_rects = [
    pygame.Rect(50, 50, 200, 50),
    pygame.Rect(50, 120, 200, 50),
    pygame.Rect(50, 190, 200, 50),
    pygame.Rect(50, 260, 200, 50),
    pygame.Rect(300, 50, 200, 50),
    pygame.Rect(300, 120, 200, 50),
    pygame.Rect(300, 190, 200, 50),
    pygame.Rect(300, 260, 200, 50)
]

button_labels = [
    "Init Repo",
    "Add All",
    "Commit",
    "Status",
    "Push",
    "Pull",
    "Create Tag",
    "View Diff"
]

button_colors = [
    GREEN,
    GREEN,
    ORANGE,
    BLUE,
    GREEN,
    PURPLE,
    GREEN,
    BLUE
]

# Zone de texte pour afficher les résultats
output_rect = pygame.Rect(50, 330, 750, 200)
input_rect = pygame.Rect(50, 540, 700, 60)
input_text = f'GIT OUTPUT CMD'

# Commandes Git associées à chaque bouton
commands = [
    "git init",
    "git add --all",
    "git commit -m 'Initial commit'",
    "git status",
    "git push --set-upstream origin main",
    "git pull origin master",
    "git tag",
    "git diff"
]

# Boucle principale
running = True
output_text = ""
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            button_index = handle_button_click(position, button_rects)
            if button_index is not None:
                # Exécuter la commande Git associée au bouton cliqué
                output_text = run_git_command(commands[button_index])
        elif event.type == VIDEORESIZE:
            WINDOW_SIZE = event.size
            screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Afficher le texte entré comme une commande (par exemple)
                output_text = run_git_command(input_text)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Remplir l'écran avec une couleur de fond
    screen.fill(DARK_GREY)

    # Dessiner les boutons
    for rect, label, color in zip(button_rects, button_labels, button_colors):
        draw_button(screen, label, rect, color)

    # Dessiner la zone de texte pour les résultats
    draw_text_box(screen, output_text, output_rect)

    # Dessiner la zone de texte d'entrée
    draw_text_box(screen, input_text, input_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()