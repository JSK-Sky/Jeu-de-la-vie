import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1200, 700))  # Fenêtre de 100x100 pixels
x, y = screen.get_size()

cellSize = 20  # Taille de chaque cellule (20x20 pixels)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 20)

running = True
cellsUpdate = False

refreshTime = 1000
lastRefreshTime = pygame.time.get_ticks()

# Dictionnaire pour stocker l'état des cellules (vivantes ou mortes)
cells = {}

# Initialisation des cellules
for i in range(0, x, cellSize):
    for j in range(0, y, cellSize):
        cells[(i, j)] = False  # Toutes les cellules sont mortes au début

# Fonction pour compter les voisins vivants d'une cellule
def getNeighborsAliveCount(cx, cy):
    count = 0
    # Vérifier tous les voisins dans les 8 directions
    for dx in [-cellSize, 0, cellSize]:
        for dy in [-cellSize, 0, cellSize]:
            if dx == 0 and dy == 0:
                continue  # Ignorer la cellule elle-même
            neighbor_x, neighbor_y = cx + dx, cy + dy
            # Vérifier que les voisins sont dans les limites de la fenêtre
            if (neighbor_x, neighbor_y) in cells and cells[(neighbor_x, neighbor_y)]:
                count += 1
    return count

def afficher_texte(Surface, texte, font, x, y, couleur=(255, 255, 255)):
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(x, y))
    Surface.blit(texte_surface, texte_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # Calculer la cellule sur laquelle on clique
            cell_x = (mx // cellSize) * cellSize
            cell_y = (my // cellSize) * cellSize
            # Inverser l'état de la cellule (vivante <-> morte)
            cells[(cell_x, cell_y)] = not cells[(cell_x, cell_y)]
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                cellsUpdate = not cellsUpdate
    # Rafraîchir l'état des cellules chaque seconde
    if cellsUpdate == True:
        refreshTime = pygame.time.get_ticks()
        if refreshTime - lastRefreshTime >= 1000:
            new_cells = {}  # Nouveau dictionnaire pour l'état des cellules
            for cx in range(0, x, cellSize):
                for cy in range(0, y, cellSize):
                    alive = cells[(cx, cy)]
                    neighbors = getNeighborsAliveCount(cx, cy)
                    if alive:
                        if neighbors < 2 or neighbors > 3:
                            new_cells[(cx, cy)] = False  # La cellule meurt
                        else:
                            new_cells[(cx, cy)] = True  # La cellule reste vivante
                    else:
                        if neighbors == 3:
                            new_cells[(cx, cy)] = True  # La cellule devient vivante
                        else:
                            new_cells[(cx, cy)] = False  # La cellule reste morte
            cells = new_cells  # Mettre à jour l'état des cellules
            lastRefreshTime = refreshTime  # Mettre à jour le temps du dernier rafraîchissement

    # Effacer l'écran
    screen.fill(WHITE)
    
    if cellsUpdate == False:
        afficher_texte(screen, "SPACE for start", font, x-x/15, y-y/20, BLACK)

    # Dessiner les cellules vivantes
    for (cx, cy), alive in cells.items():
        if alive:
            pygame.draw.rect(screen, BLACK, (cx, cy, cellSize, cellSize))  # Dessiner un rectangle pour chaque cellule vivante

    pygame.display.flip()  # Mettre à jour l'affichage

pygame.quit()
